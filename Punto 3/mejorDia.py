from mrjob.job import MRJob
from mrjob.step import MRStep

class mejorDia(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            rating = filing[2]
            fecha = filing[4]
            yield fecha, float(rating)

    def reducer(self, key, values):
        ratingTotal = 0
        count = 0

        for rating in values:
            ratingTotal += rating
            count += 1

        ratingProm = ratingTotal / count

        yield None, (ratingProm, key)  

    def encontrarMayor(self, _, values):
        mayorProm = 0
        mayorFecha = None

        for ratingProm, fecha in values:
            if ratingProm > mayorProm:
                mayorProm = ratingProm
                mayorFecha = fecha

        yield mayorFecha, mayorProm

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.encontrarMayor)
        ]

if __name__ == '__main__':
    mejorDia.run()