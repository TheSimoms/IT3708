package ex1;

public class Exercise {
    public static void main(String[] args) {
        World world = new World(1024, 576);

        world.addRandomObstacle();
        world.addRandomPredator();
        world.addRandomBoids(Config.NUMBER_OF_BOIDS);
    }
}
