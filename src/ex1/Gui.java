package ex1;

import javafx.animation.AnimationTimer;
import javafx.animation.Timeline;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.shape.ArcType;
import javafx.stage.Stage;

public class Gui {
    private World world;
    private GraphicsContext gc;

    public Gui (World world) {
        this.world = world;
    }

    public void start (Stage primaryStage) {
        Group root = new Group();
        Scene scene = new Scene(root);

        primaryStage.setTitle("Flocking and Avoidance With Boids");
        primaryStage.setScene(scene);

        Canvas canvas = new Canvas(world.getWidth(), world.getHeight());

        root.getChildren().add(canvas);

        gc = canvas.getGraphicsContext2D();

        new AnimationTimer () {
            public void handle (long currentNanoTime) {
                gc.clearRect(0, 0, world.getWidth(), world.getHeight());

                world.updateNeighbourLists();
                world.updateObjectMoves();
                world.performMoves();

                drawObjects();
            }
        }.start();

        primaryStage.show();
    }

    private void drawBoids () {
        gc.setFill(Color.BLUE);

        for (Boid boid : world.getBoids()) {
            gc.fillOval(boid.getX(), boid.getY(), Config.BOID_RADIUS, Config.BOID_RADIUS);
        }
    }

    private void drawPredators () {
        gc.setFill(Color.RED);

        for (Predator predator : world.getPredators()) {
            gc.fillOval(predator.getX(), predator.getY(), Config.PREDATOR_RADIUS, Config.PREDATOR_RADIUS);
        }
    }

    private void drawObstacles () {
        gc.setFill(Color.GREEN);

        for (Obstacle obstacle : world.getObstacles()) {
            gc.fillOval(obstacle.getX(), obstacle.getY(), Config.OBSTACLE_RADIUS, Config.OBSTACLE_RADIUS);
        }
    }

    private void drawObjects () {
        drawBoids();
        drawPredators();
        drawObstacles();
    }

    private void drawBoids(GraphicsContext gc) {
        gc.setFill(Color.GREEN);
        gc.setStroke(Color.BLUE);
        gc.setLineWidth(5);
        gc.strokeLine(40, 10, 10, 40);
        gc.fillOval(10, 60, 30, 30);
        gc.strokeOval(60, 60, 30, 30);
        gc.fillRoundRect(110, 60, 30, 30, 10, 10);
        gc.strokeRoundRect(160, 60, 30, 30, 10, 10);
        gc.fillArc(10, 110, 30, 30, 45, 240, ArcType.OPEN);
        gc.fillArc(60, 110, 30, 30, 45, 240, ArcType.CHORD);
        gc.fillArc(110, 110, 30, 30, 45, 240, ArcType.ROUND);
        gc.strokeArc(10, 160, 30, 30, 45, 240, ArcType.OPEN);
        gc.strokeArc(60, 160, 30, 30, 45, 240, ArcType.CHORD);
        gc.strokeArc(110, 160, 30, 30, 45, 240, ArcType.ROUND);
        gc.fillPolygon(new double[]{10, 40, 10, 40},
                new double[]{210, 210, 240, 240}, 4);
        gc.strokePolygon(new double[]{60, 90, 60, 90},
                new double[]{210, 210, 240, 240}, 4);
        gc.strokePolyline(new double[]{110, 140, 110, 140},
                new double[]{210, 210, 240, 240}, 4);
    }
}
