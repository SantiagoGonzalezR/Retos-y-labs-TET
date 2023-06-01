from mrjob.job import MRJob
from mrjob.step import MRStep
class diaNegro(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            yield filing[0], (float(filing[1]), filing[2])

    def reducer(self, key, values):
        precios = list(values)
        precioMin = min(precios, key=lambda x: x[0])
        yield precioMin[1], 1

    def menoresPrecios(self, key, values):
        count = sum(values)
        maxCount = 0
        diaMax = None

        if count > maxCount:
            maxCount = count
            diaMax = key

        yield None, (diaMax, maxCount) 

    def diaMax(self, _, pairs):
        diaMaximo = None
        maxCount = 0

        for day, counter in pairs:
            if counter > maxCount:
                maxCount = counter
                diaMaximo = day

        yield diaMaximo, maxCount

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.menoresPrecios),
            MRStep(reducer=self.diaMax)
        ]

if __name__ == '__main__':
    diaNegro.run()