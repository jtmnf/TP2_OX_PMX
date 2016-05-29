import json
import time

class File:

    @staticmethod
    def writeToFile(Config, Recombination, Problem, StatBestByRun, StatAvgBestByRun, Time, BestRun):
        timestamp = time.gmtime()
        timestamp = '' + str(timestamp.tm_mday) + '_' + str(timestamp.tm_hour) + '_' + str(timestamp.tm_min)

        fileName = \
            Problem['name'] + "_" + \
            Recombination['name'] + "_" + \
            str(Problem['config']['cromo_size']) + "_" + \
            timestamp


        path = 'Results/'
        f = open(path + fileName + ".txt", 'w')

        num = json.dumps({'Num_generations': Config['numb_generations']})
        pop = json.dumps({'Pop_size': Config['pop_size']})
        run = json.dumps({'Runs': Config['runs']})
        tim = json.dumps({'Time': Time})
        bes = json.dumps({'BestRun': BestRun})
        statBest = json.dumps({'StatBestByRun': StatBestByRun})
        statAvg = json.dumps({'StatAvgBestByRun': StatAvgBestByRun})

        f.write(
            num + "\n" +
            pop + "\n" +
            run + "\n" +
            tim + "\n" +
            bes + "\n" +
            statBest + "\n" +
            statAvg + "\n")

        f.close()