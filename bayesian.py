#!/usr/bin/env python3

import sys
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor

from adaptivecrawler import FixedKeyword, SampleStream
from enrichment import Enrichment
from sink import sink_null, sink_stdout
from utils import read_config, coroutine, threadsafe_generator, CRAWLER_STATUS, AGGREGATE_STATUS


POOL = ThreadPoolExecutor()

class BayesianAdaptation(object):
    '''
    Exploiting sample stream for Adaptive Microblog Crawling.
    Bayesian Adaptation: A Bayesian approach to adaptive microblog crawling.
    '''
    def __init__(self, *args, **kwargs):
        pass

    def run(self):
        params = read_config()
        self.likelihood = params['likelihood']
        #e = Enrichment(name, sink_null()).enrich()
        s = sink_stdout()
        b = self.bayesian_aggregator()
        name   = 'sample_stream_' + params['seed']

        name = params['seed'] + '_filter_stream'
        CRAWLER_STATUS[name] = ('run', None)
        future = POOL.submit(FixedKeyword(name=name, twitter_key=3, **params).run, s, b)
        future.add_done_callback(self.result_handler)

        s = sink_null()
        name = params['seed'] + '_sample_stream'
        CRAWLER_STATUS[name] = ('run', None)
        future = POOL.submit(SampleStream(name=name, twitter_key=1, **params).run, s, b)
        future.add_done_callback(self.result_handler)

    def result_handler(self, fut):
        print(fut.result())

    def gen_hashtags(self, hts, sample_freq, filter_freq):
        return hts
        hts = {}
        sample_total = sum([sample_freq[ht] for ht in hts])
        filter_total = sum([filter_freq[ht] for ht in hts])
        for ht in hashtags:
            sample_prob = sample_freq[ht] / sample_total
            filter_prob = filter_freq[ht] / filter_total
            if (filter_prob - sample_prob) >= self.likelihood:
                hts.add(ht)
        return hts

    def update_status(self, streams):
        '''Selects up to k top hashtags for the next iteration
        under the following rquirements:
        - hashtags are not in blocked list
        - hashtags are above minimum frequency
        '''
        for stream in streams:
            crawler = stream['crawler']
            if crawler == 'SampleStream':
                sample_freq = stream['frequency']
                sample_hashtags  = set(stream['hashtags'].split())
            elif crawler == 'FixedKeyword':
                filter_freq = stream['frequency']
                filter_hashtags = set(stream['hashtags'].split())
            else:
                sys.stderr.write('Encountered unknown crawler {}.\n'.format(crawler))
        candidate_hashtags = filter_hashtags.intersection(sample_hashtags)
        updated_hashtags = self.gen_hashtags(candidate_hashtags, sample_freq, filter_freq)
        if updated_hashtags - self.H != set([]):
            action = 'update'
            self.H = updated_hashtags.union(self.H)
        else:
            action = 'run'
        for stream in streams:
            name = stream['name']
            CRAWLER_STATUS[name]   = (action, hashtags)
            AGGREGATE_STATUS[name] = 'done'
            sys.stderr.write('{} {} {} {}\n'.format(time.asctime(), name, action, ' '.join(self.H)))


    @threadsafe_generator
    @coroutine
    def bayesian_aggregator(self):
        ''' framework to compute the posterior probability of hashtags if
        the posterior probability of a given hashtag is more than a
        threshold then the hashtag is considered for a query in the next
        iteration.
        '''
        stats = []
        while True:
            res = (yield)
            stats.append(res)
            if len(stats) != 2 : continue
            #sys.stderr.write('{}\n'.format(json.dumps(stats)))
            self.update_status(stats)
            stats = []


def main():
    b = BayesianAdaptation()
    b.run()


if __name__ == '__main__':
    main()
