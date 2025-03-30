
class CPU:
    def __init__(self, level, player, enemy):
        self.level = level
        self.player = player
        self.enemy = enemy

    def track_enemy(self):
        if self.enemy.x > self.player.x:
            self.player.move_right()
        if self.enemy.x < self.player.x:
            self.player.move_left()
        if self.enemy.y < self.player.y and self.player.jumps <= self.player.jump_limit:
            self.player.jump()
            self.player.update()

    def retreat(self):
        if self.enemy.x > self.player.x:
            self.player.move_left()
        if self.enemy.x < self.player.x:
            self.player.move_right()
        if self.enemy.y < self.player.y and self.player.jumps <= self.player.jump_limit:
            self.player.jump()


    def update(self):
        if self.player.speed_x > 0:
            if self.player.speed_x < self.enemy.speed_x:
                self.retreat()
            else:
                self.track_enemy()
        else:
            if self.player.speed_x > self.enemy.speed_x:
                self.retreat()
            else:
                self.track_enemy()
