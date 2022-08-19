class obj(object):
    def __init__(this, filename):
        with open(filename) as f:
            this.lines = f.read().splitlines()

        this.vertices = []
        this.faces = []
        this.read()

    def read(this):
        for line in this.lines:
            if line:
                prefix, value = line.split(' ', 1)

                if prefix == 'v':
                    this.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    this.faces.append([list(map(int , face.split('/'))) for face in value.split(' ')])

