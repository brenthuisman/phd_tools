#!/usr/bin/env python
import sys,rtplan

rtplan = rtplan.rtplan(sys.argv[-1])
rtplan.savelayerhistos()
rtplan.savespothistos()

