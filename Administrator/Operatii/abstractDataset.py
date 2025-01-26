from torch.utils.data import Dataset, DataLoader, ConcatDataset

class Dataset(object):
    def __getitem__(self, index):
        raise NotImplementedError
    
    def __len__(self):
        raise NotImplementedError
    
    def __add__(self, other):
        raise ConcatDataset([self,other])
    