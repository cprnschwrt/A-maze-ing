from pydantic import BaseModel, model_validator


class Vector2(BaseModel):
    x: int
    y: int

    def __str__(self):
        return f"{self.x, self.y}"


class MazePart(BaseModel):
    position: Vector2
    active: bool = True

    def __str__(self):
        return str(0 if not self.active else 1)


class MazeGrid(BaseModel):
    x: int
    y: int
    objects: list = []

    @model_validator(mode="after")
    def init(self):
        for x in range(self.x):
            list.append(self.objects, [])
            for y in range(self.y):
                self.objects[x].append(MazePart(position=Vector2(x=x, y=y)))
                print(self.objects[x][y], end="")
            print()
        return self

    def __len__(self):
        return f"{self.x, self.y}"


grid = MazeGrid(x=10, y=10)
