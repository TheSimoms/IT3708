package ex1;

import javafx.animation.AnimationTimer;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.image.Image;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

public class Gui {
    private World world;
    private GraphicsContext gc;

    private Image boidImage = new Image("figures/boid.png");
    private Image boidAvoidingImage = new Image("figures/boid_avoiding.png");

    public Gui (World world) {
        this.world = world;
    }

    public void start (Stage primaryStage) {
        Group root = new Group();
        Scene scene = new Scene(root);

        primaryStage.setTitle("Flocking and Avoidance With Boids");
        primaryStage.setScene(scene);

        Canvas canvas = new Canvas(world.getWidth(), world.getHeight()+300);

        root.getChildren().add(canvas);

        gc = canvas.getGraphicsContext2D();

        new AnimationTimer () {
            public void handle (long currentNanoTime) {
                gc.clearRect(0, 0, world.getWidth(), world.getHeight() + Config.NEIGHBOURHOOD_RADIUS);

                gc.strokeRect(0, 0, world.getWidth(), world.getHeight());

                world.updateNeighbourLists();
                world.updateObjectMoves();
                world.performMoves();

                drawObjects();
            }
        }.start();

        primaryStage.show();
    }

    public void drawCircle (double x, double y, double radius) {
        gc.fillOval(x - radius, y - radius, radius * 2, radius * 2);
    }

    public void drawImage (Image image, double x, double y, double radius, double rotation) {
        gc.save();

        gc.translate(x, y);
        gc.rotate(rotation * Math.PI/180);
        gc.drawImage(image, -radius, -radius, radius * 2, radius * 2);

        gc.restore();
    }

    public void drawMovableObject (Image image, MovableWorldObject movableWorldObject) {
        drawImage(image,
                movableWorldObject.getX(),
                movableWorldObject.getY(),
                movableWorldObject.getRadius(),
                Maths.vectorDirection(movableWorldObject.getVelocity()));
    }

    private void drawBoids () {
        if (!Config.DEBUG) {
            gc.setFill(Color.BLUE);
        }

        for (Boid boid : world.getBoids()) {
            if (boid.isDead()) {
                if (Config.DEBUG) {
                    if (gc.getFill() != Color.BLACK) {
                        gc.setFill(Color.BLACK);
                    }

                    drawCircle(boid.getX(), boid.getY(), boid.getRadius());
                }
            } else {
                if (Config.DEBUG) {
                    gc.setFill(Color.PURPLE);

                    gc.setGlobalAlpha(0.1);
                    drawCircle(boid.getX(), boid.getY(), Config.NEIGHBOURHOOD_RADIUS);
                    gc.setGlobalAlpha(1.0);

                    if (boid.isAvoiding()) {
                        drawMovableObject(boidAvoidingImage, boid);
                    } else {
                        drawMovableObject(boidImage, boid);
                    }
                } else {
                    drawMovableObject(boidImage, boid);
                }
            }
        }
    }

    private void drawPredators () {
        gc.setFill(Color.RED);

        for (Predator predator : world.getPredators()) {
            drawCircle(predator.getX(), predator.getY(), predator.getRadius());
        }
    }

    private void drawObstacles () {
        gc.setFill(Color.GREEN);

        for (Obstacle obstacle : world.getObstacles()) {
            drawCircle(obstacle.getX(), obstacle.getY(), obstacle.getRadius());
        }
    }

    private void drawObjects () {
        drawBoids();
        drawPredators();
        drawObstacles();
    }
}
