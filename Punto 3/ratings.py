from mrjob.job import MRJob

class ratings(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            usuario= filing[0] 
            rating= filing[2]
            yield usuario, float(rating)

    def reducer(self, key, values):
        ratingTotal= 0
        count = 0

        for rating in values:
            ratingTotal += rating
            count += 1

        ratingProm = ratingTotal / count

        yield key, (ratingProm,count)
if __name__ == '__main__':
    ratings.run()