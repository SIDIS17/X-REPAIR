import math
import unittest
from backend.modules import vibe, acoustic, thermal, power, circuit, core

class XRepairTests(unittest.TestCase):
    def test_vibe(self):
        fs=256; rpm=1500; f=rpm/60
        s=[math.sin(2*math.pi*f*k/fs) for k in range(256)]
        r=vibe.analyze(s,fs,rpm)
        self.assertIn("health_score",r)

    def test_acoustic(self):
        s=[math.sin(2*math.pi*20*k/256) for k in range(256)]
        self.assertIn("diagnostic",acoustic.analyze(s,256))

    def test_thermal(self):
        r=thermal.analyze([30,35,40],25,80)
        self.assertEqual(r["diagnostic"],"thermique_normal")

    def test_power(self):
        n=128; fs=1280; f=50
        v=[325*math.sin(2*math.pi*f*k/fs) for k in range(n)]
        i=[4*math.sin(2*math.pi*f*k/fs) for k in range(n)]
        r=power.analyze(v,i,230)
        self.assertGreater(r["features"]["power_factor"],0.9)

    def test_circuit(self):
        net="V1 in 0 12\nR1 in 0 1k\n.op\n.end"
        r=circuit.analyze(net,False)
        self.assertEqual(r["components"]["resistors"],1)

    def test_core(self):
        r=core.fuse({"vibe":{"health_score":80},"thermal":{"health_score":90}})
        self.assertGreater(r["health_score"],0)

if __name__=="__main__":
    unittest.main()
