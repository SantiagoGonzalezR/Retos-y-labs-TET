from mrjob.job import MRJob
from mrjob.step import MRStep

class mayorDia(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            fecha= filing[4]
            yield fecha, 1

    def reducer(self, key, values):
        vistas = sum(values)
        yield None, (vistas, key)

    def encontrarMax(self, _, fechas_y_visualizaciones):
        vistasMax = 0
        fechaMax = None
        for fechaVis in fechas_y_visualizaciones:
            vistas, fecha = fechaVis
            if vistas > vistasMax:
                vistasMax = vistas
                fechaMax = fecha
        yield fechaMax, vistasMax

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.encontrarMax)
        ]

if __name__ == '__main__':
    mayorDia.run()