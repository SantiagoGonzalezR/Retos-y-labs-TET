from mrjob.job import MRJob

class accionMinMax(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            yield filing[0],(float(filing[1]), filing[2])
    
    def reducer(self, key, values):
        precios = list(values)
        preciosMin = min(precios)
        preciosMax = max(precios)
        yield key, (preciosMin[1],preciosMax[1])

if __name__ == '__main__':
    accionMinMax.run()