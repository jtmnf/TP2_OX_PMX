import matplotlib.pyplot as plt

class Visual:
    @staticmethod
    def plotBestAverage(StatBestByRun, StatAvgBestByRun, store='no_store', figure_legend='none'):
        ax1 = plt.subplot(1, 1, 1)

        generations = list(range(len(StatBestByRun)))
        ax1.plot(generations, StatBestByRun, label="Best Overall")
        ax1.plot(generations, StatAvgBestByRun, label="Best Average")

        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Performance over runs')
        plt.legend(loc='best')

        plt.legend(loc='upper right')

        if(store == 'store'):
            plt.savefig("Results/" + figure_legend + ".png")
        else:
            plt.show()

        plt.close()
