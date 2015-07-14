import matplotlib.pyplot as plt

cdict3 = {'red':  ((0.0, 0.0, 0.0),
                   (0.25, 1.0, 1.0),
                   (0.5, 1.0, 0.0),
                   (0.75, 0.0, 0.0),
                   (1.0, 0.9, 0.9)),

         'green': ((0.0, 1.0, 1.0),
                   (0.25, 1.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (0.75, 1.0, 1.0),
                   (1.0, 0.9, 0.9)),

         'blue':  ((0.0, 0.0, 0.0),
                   (0.5, 0.0, 1.0),
                   (1.0, 1.0, 1.0))
        }
plt.register_cmap(name='SD_V', data=cdict3)


if __name__=="__main__" :
  import pylab as p
  x = p.arange(0, p.pi, 0.1)
  y = p.arange(0, 2*p.pi, 0.1)
  X, Y = p.meshgrid(x,y)
  Z = p.cos(X) * p.sin(Y)
  p.imshow(Z, interpolation='nearest', cmap='SD_V')
  p.colorbar()
  p.show()
 
