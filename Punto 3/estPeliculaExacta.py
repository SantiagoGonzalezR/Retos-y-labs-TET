from mrjob.job import MRJob

class estPeliculaExcta(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            peli= filing[1] 
            rating= filing[2]
            yield peli, float(rating)

    def reducer(self, key, values):
        ratingTotal= 0
        count = 0

        for rating in values:
            ratingTotal += rating
            count += 1

        ratingProm = ratingTotal / count

        yield key, (ratingProm,count)

if __name__ == '__main__':
    estPeliculaExcta.run()