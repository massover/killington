from ..factories import LotteryFactory


def test_lottery_url():
    lottery = LotteryFactory.build()
    assert str(lottery.lottery_id) in lottery.url


def test_lottery_http_referer():
    lottery = LotteryFactory.build()
    assert str(lottery.lottery_id) in lottery.http_referer