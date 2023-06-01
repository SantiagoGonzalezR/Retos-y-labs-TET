from mrjob.job import MRJob
from mrjob.step import MRStep

class mejorPeor(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            peli = filing[1] 
            rating = filing[2]
            genero = filing[3]
            yield genero, (float(rating), peli)

    def reducer(self, key, values):
        ratings = list(values)
        menor = min(ratings)
        mayor = max(ratings)
        yield key, (menor[1],mayor[1])

if __name__ == '__main__':
    mejorPeor.run()