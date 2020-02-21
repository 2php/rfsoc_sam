from pynq import DefaultIP
from pynq import DefaultHierarchy
from pynq import Xlnk
import numpy as np

class SpectrumAverage(DefaultHierarchy):

    def __init__(self, description):
        super().__init__(description)
        
        self.FrameMovingAverage.reset = 1
        self.FrameMovingAverage.num = 1
        self.FrameMovingAverage.div = pow(2,30) # divider reads in as u32_30
        self.FrameMovingAverage.reset = 0
        
    @staticmethod
    def checkhierarchy(description):
        if 'FrameMovingAverage' in description['ip']:
            return True
        return False 

class DataInspectorCore(DefaultIP):
    """Driver for Data Inspector's core logic IP
    Exposes all the configuration registers by name via data-driven properties
    """
    
    def __init__(self,description):
        super().__init__(description=description)
        
    bindto = ['UoS:RFSoC:FrameMovingAverage:0.2']
    
    
# LUT of property addresses for our data-driven properties
_dataInspector_props = [("num", 0x100), ("div", 0x104), ("reset", 0x108)]

# Func to return a MMIO getter and setter based on a relative addr
def _create_mmio_property(addr):
    def _get(self):
        return self.read(addr)

    def _set(self, value):
        self.write(addr, value)

    return property(_get, _set)


# Generate getters and setters based on _dataInspector_props
for (name, addr) in _dataInspector_props:
    setattr(DataInspectorCore, name, _create_mmio_property(addr))