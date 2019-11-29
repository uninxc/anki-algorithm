#!/usr/bin/env python
# encoding: utf-8
import random
import time

from card import Card
from config import Config


class Scheduler:

    def __init__(self):
        self.config = Config()
        self.m = 1

    def next_review(self, card, ease):
        """
        :param card:
        :param ease: 必须大于1
        :return:
        """

        assert 1 < ease <= 4
        delay = self._days_late(card)
        fct = card.factor / 1000

        ivl2 = self._constrainedIvl((card.ivl + delay // 4) * 1.2 * self.m, card.ivl)
        ivl3 = self._constrainedIvl((card.ivl + delay // 2) * fct * self.m, ivl2)
        ivl4 = self._constrainedIvl((card.ivl + delay) * fct * self.m * self.config['ease4'], ivl3)

        print(">>>>>>>>> {0}, {1}, {2} ".format(ivl2, ivl3, ivl4))

        if ease == 2:
            interval = ivl2
        elif ease == 3:
            interval = ivl3
        elif ease == 4:
            interval = ivl4

        self._change_factor(ease, card)

        iv = min(interval, self.config['maxIvl'])
        card.reps = card.reps + 1
        card.ivl = self._fuzzedIvl(iv)
        card.due = int((time.time() - card.get_review_time()) // 86400) + iv

        print("fuzz result: " + str(card.ivl))
        return iv

    def next_review_hard(self, card, ease):
        assert 1 == ease
        card.lapses += 1
        card.ivl = self._nextLapseIvl(card, self.config)
        self._change_factor(card, ease)
        card.due = int((time.time() - card.get_review_time()) // 86400) + card.ivl

    def _nextLapseIvl(self, card, conf):
        return max(conf['minInt'], int(card.ivl*conf['mult']))

    def _change_factor(self, ease, cards):
        if ease == 1:
            cards.factor = max(1300, card.factor - 200)
        elif ease == 2:
            cards.factor = max(1300, card.factor - 150)
        elif ease == 3:
            pass
        elif ease == 4:
            cards.factor = max(1300, card.factor + 150)

        print("The factor now is " + str(card.factor))

    def _constrainedIvl(self, ivl, prev):
        new = ivl * self.config.get('ivlFct', 1)
        return int(max(new, prev+1))

    def _days_late(self, cards):
        delay = max(0, int((time.time() - cards.get_review_time()) // 86400) - card.due)
        print("Delay: " + str(delay))
        return delay

    def _fuzzedIvl(self, ivl):
        min, max = self._fuzzIvlRange(ivl)
        return random.randint(min, max)

    def _fuzzIvlRange(self, ivl):
        if ivl < 2:
            return [1, 1]
        elif ivl == 2:
            return [2, 3]
        elif ivl < 7:
            fuzz = int(ivl * 0.25)
        elif ivl < 30:
            fuzz = max(2, int(ivl * 0.15))
        else:
            fuzz = max(4, int(ivl * 0.05))
        # fuzz at least a day
        fuzz = max(fuzz, 1)
        return [ivl - fuzz, ivl + fuzz]


if __name__ == '__main__':
    card = Card()
    card.factor = 2500
    card.reviewTime = 1575011498
    card.ivl = 1
    card.due = 1

    sche = Scheduler()

    while(True):
        ease = int(input('Input ease in (1, 2, 3, 4): '))
        if ease == 1:
            sche.next_review_hard(card, ease)
        else:
            sche.next_review(card, ease)
            print("It must be learn again, right now!")
        print(card.__dict__)
        print('First time: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(card.reviewTime)))
        print('Right time: ' +  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print("===================================================================")





