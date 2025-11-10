def render(self):
    if self.screen is None:
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Fauteuil Roulant")
        self.clock = pygame.time.Clock()

    self.screen.fill((255, 255, 255))
    pygame.draw.rect(self.screen, (0, 0, 0), (250, 250, 100, 100))  # Carré test
    pygame.display.flip()
    self.clock.tick(30)
    # Pas de return ici !
