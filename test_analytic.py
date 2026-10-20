from analytic_model import analyticModel

def test_lectureExample():
    # приклад з лекції 8: автосервіс, 3 бригади, lambda = 7, t = 0,75 год, m = 4
    r = analyticModel(3, lam=7, mu=1 / 0.75, m=4)

    assert round(r["q0"], 6) == 0.001939
    assert round(r["pQueue"], 6) == 0.522505
    assert round(r["pRefusal"], 6) == 0.438649
    assert round(r["Q"], 6) == 0.561351
    assert round(r["A"], 3) == 3.929
    assert round(r["nBusy"], 3) == 2.947
    assert round(r["Lq"], 3) == 2.875
    assert round(r["Ls"], 3) == 5.822


def test_probabilities():
    for c in range(1, 7):
        r = analyticModel(c)
        assert 0 < r["q0"] < 1
        assert 0 < r["pRefusal"] < 1
        assert r["nBusy"] <= c


if __name__ == "__main__":
    test_lectureExample()
    test_probabilities()
    print("Усі перевірки пройдено")