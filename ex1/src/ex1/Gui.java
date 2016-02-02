package ex1;

import javafx.animation.AnimationTimer;
import javafx.event.EventHandler;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.MouseEvent;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

public class Gui {
    private World world;
    private GraphicsContext gc;

    private final Color boidColor = Color.BLUE;
    private final Color boidAvoidingColor = Color.YELLOW;
    private final Color boidDeadColor = Color.BLACK;
    private final Color boidNeighbourColor = Color.PURPLE;
    private final Color predatorColor = Color.RED;
    private final Color obstacleColor = Color.GREEN;
    private final Color textColor = Color.BLACK;

    private double verticalMargin = 200.0;

    public Gui (World world) {
        this.world = world;
    }

    private void drawButton (double x, double y, boolean plus) {
        gc.strokeRect(x, y, 35, 35);

        gc.strokeLine(x + 5, y + 35 / 2, x + 30, y + 35 / 2);

        if (plus) {
            gc.strokeLine(x + 35 / 2, y + 5, x + 35 / 2, y + 30);
        }
    }

    private void setupButtons () {
        gc.setFill(textColor);
        gc.setStroke(Color.BLACK);

        gc.fillText("Alignment weight", 20, 20);
        gc.fillText("Separation weight", 20, 60);
        gc.fillText("Cohesion weight", 20, 100);

        drawButton(160, 5, true);
        drawButton(160, 45, true);
        drawButton(160, 85, true);

        drawButton(220, 5, false);
        drawButton(220, 45, false);
        drawButton(220, 85, false);

        gc.fillText("Predators", 500, 20);
        gc.fillText("Obstacles", 500, 60);

        drawButton(600, 5, true);
        drawButton(600, 45, true);

        drawButton(660, 5, false);
        drawButton(660, 45, false);

    }

    private void drawForces () {
        gc.clearRect(275, 10, 50, 120);

        gc.fillText(String.valueOf(world.getForces().get(0).getWeight()), 280, 30);
        gc.fillText(String.valueOf(world.getForces().get(1).getWeight()), 280, 70);
        gc.fillText(String.valueOf(world.getForces().get(2).getWeight()), 280, 110);
    }

    private boolean isHittingButton (MouseEvent mouseEvent, double x, double y) {
        return mouseEvent.getX() >= x && mouseEvent.getX() <= x + 35 && mouseEvent.getY() >= y && mouseEvent.getY() <= y + 35;
    }

    private double increaseValue (double value) {
        return Math.min(value + 1.0, Config.FORCE_MAX_WEIGHT);
    }

    private double decreaseValue (double value) {
        return Math.max(value - 1.0, 0.0);
    }

    public void start (Stage primaryStage) {
        Group root = new Group();
        Scene scene = new Scene(root);

        primaryStage.setTitle("Flocking and Avoidance With Boids");
        primaryStage.setScene(scene);

        Canvas canvas = new Canvas(world.getWidth(), world.getHeight() + verticalMargin);

        root.getChildren().add(canvas);

        gc = canvas.getGraphicsContext2D();

        gc.setStroke(Color.BLACK);

        setupButtons();

        scene.addEventFilter(MouseEvent.MOUSE_PRESSED, new EventHandler<MouseEvent>() {
            @Override
            public void handle (MouseEvent mouseEvent) {
                if (mouseEvent.getX() >= 160 && mouseEvent.getX() <= 255 && mouseEvent.getY() >= 5 && mouseEvent.getY() <= 120) {
                    Force force = null;
                    boolean increase;

                    if (isHittingButton(mouseEvent, 160, 5)) {
                        force = world.getForces().get(0);
                        increase = true;
                    } else if (isHittingButton(mouseEvent, 160, 45)) {
                        force = world.getForces().get(1);
                        increase = true;
                    } else if (isHittingButton(mouseEvent, 160, 85)) {
                        force = world.getForces().get(2);
                        increase = true;
                    } else if (isHittingButton(mouseEvent, 220, 5)) {
                        force = world.getForces().get(0);
                        increase = false;
                    } else if (isHittingButton(mouseEvent, 220, 45)) {
                        force = world.getForces().get(1);
                        increase = false;
                    } else if (isHittingButton(mouseEvent, 220, 85)) {
                        force = world.getForces().get(2);
                        increase = false;
                    } else {
                        increase = false;
                    }

                    if (force != null) {
                        if (increase) {
                            force.setWeight(increaseValue(force.getWeight()));
                        } else {
                            force.setWeight(decreaseValue(force.getWeight()));
                        }
                    }
                } else if (isHittingButton(mouseEvent, 600, 5)) {
                    world.addRandomPredator();
                } else if (isHittingButton(mouseEvent, 660, 5)) {
                    world.removePredators();
                } else if (isHittingButton(mouseEvent, 600, 45)) {
                    world.addRandomObstacle();
                } else if (isHittingButton(mouseEvent, 660, 45)) {
                    world.removeObstacles();
                }
            }
        });

        new AnimationTimer () {
            public void handle (long currentNanoTime) {
                gc.clearRect(0, verticalMargin, world.getWidth(), world.getHeight());
                gc.strokeRect(0, verticalMargin, world.getWidth(), world.getHeight());

                world.updateNeighbourLists();
                world.updateObjectMoves();
                world.performMoves();

                drawObjects();
                drawForces();

                gc.clearRect(0, verticalMargin - Config.NEIGHBOURHOOD_RADIUS, world.getWidth(), Config.NEIGHBOURHOOD_RADIUS);
            }
        }.start();

        primaryStage.show();
    }

    public void drawCircle (double x, double y, double radius) {
        gc.fillOval(x - radius, verticalMargin + y - radius, radius * 2, radius * 2);
    }

    public void drawMovableObject (MovableWorldObject object) {
        drawCircle(object.getX(), object.getY(), object.getRadius());

        gc.strokeLine(object.getX(), verticalMargin + object.getY(), object.getX() + object.getvX(), verticalMargin + object.getY() + object.getvY());
    }

    private void drawBoids () {
        for (Boid boid : world.getBoids()) {
            gc.setFill(boidColor);

            if (boid.isDead()) {
                if (Config.DEBUG) {
                    gc.setFill(boidDeadColor);
                } else {
                    continue;
                }
            } else {
                if (Config.DEBUG) {
                    gc.setFill(boidNeighbourColor);

                    gc.setGlobalAlpha(0.1);
                    drawCircle(boid.getX(), boid.getY(), Config.NEIGHBOURHOOD_RADIUS);
                    gc.setGlobalAlpha(1.0);

                    gc.setFill(boidColor);

                    if (boid.isAvoiding()) {
                        gc.setFill(boidAvoidingColor);
                    }
                }
            }

            drawMovableObject(boid);
        }
    }

    private void drawPredators () {
        gc.setFill(predatorColor);

        for (Predator predator : world.getPredators()) {
            drawMovableObject(predator);
        }
    }

    private void drawObstacles () {
        gc.setFill(obstacleColor);

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
