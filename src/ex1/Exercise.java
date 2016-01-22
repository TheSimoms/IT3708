package ex1;

import javafx.application.Application;
import javafx.stage.Stage;

public class Exercise extends Application {
    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        World world = new World(Config.WIDTH, Config.HEIGHT);
        Gui gui = new Gui(world);

        world.addForce(new ForceAlignment(world, Config.ALIGNMENT_WEIGHT));
        world.addForce(new ForceCohesion(world, Config.COHESION_WEIGHT));
        world.addForce(new ForceAvoidance(world, Config.AVOIDANCE_WEIGHT));
        world.addForce(new ForceFlight(world, Config.FLIGHT_WEIGHT));
        world.addForce(new ForceSeparation(world, Config.SEPARATION_WEIGHT));

        world.addRandomObstacle();
        world.addRandomPredator();
        world.addRandomBoids(Config.NUMBER_OF_BOIDS);

        gui.start(primaryStage);
    }
}
