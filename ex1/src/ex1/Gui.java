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

        gc.fillText("Alignment weight", 20, 25);
        gc.fillText("Separation weight", 20, 65);
        gc.fillText("Cohesion weight", 20, 105);

        drawButton(160, 10, true);
        drawButton(160, 50, true);
        drawButton(160, 90, true);

        drawButton(220, 10, false);
        drawButton(220, 50, false);
        drawButton(220, 90, false);

        gc.fillText("Predators", 500, 25);
        gc.fillText("Obstacles", 500, 65);

        drawButton(600, 10, true);
        drawButton(600, 50, true);

        drawButton(660, 10, false);
        drawButton(660, 50, false);

    }

    private void drawForces () {
        gc.clearRect(275, 10, 50, 120);

        gc.fillText(String.valueOf(world.getForces().get(0).getWeight()), 280, 35);
        gc.fillText(String.valueOf(world.getForces().get(1).getWeight()), 280, 75);
        gc.fillText(String.valueOf(world.getForces().get(2).getWeight()), 280, 115);
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
                if (mouseEvent.getX() >= 160 && mouseEvent.getX() <= 255 && mouseEvent.getY() >= 10 && mouseEvent.getY() <= 125) {
                    Force force = null;
                    boolean increase;

                    if (isHittingButton(mouseEvent, 160, 10)) {
                        force = world.getForces().get(0);
                        increase = true;
                    } else if (isHittingButton(mouseEvent, 160, 50)) {
                        force = world.getForces().get(1);
                        increase = true;
                    } else if (isHittingButton(mouseEvent, 160, 90)) {
                        force = world.getForces().get(2);
                        increase = true;
                    } else if (isHittingButton(mouseEvent, 220, 10)) {
                        force = world.getForces().get(0);
                        increase = false;
                    } else if (isHittingButton(mouseEvent, 220, 50)) {
                        force = world.getForces().get(1);
                        increase = false;
                    } else if (isHittingButton(mouseEvent, 220, 90)) {
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
                } else if (mouseEvent.getX() >=  600 && mouseEvent.getX() <= 635 && mouseEvent.getY() >= 10 && mouseEvent.getY() <= 45) {
                    world.addRandomPredator();
                } else if (mouseEvent.getX() >=  660 && mouseEvent.getX() <= 695 && mouseEvent.getY() >= 10 && mouseEvent.getY() <= 45) {
                    world.removePredators();
                } else if (mouseEvent.getX() >=  600 && mouseEvent.getX() <= 635 && mouseEvent.getY() >= 50 && mouseEvent.getY() <= 85) {
                    world.addRandomObstacle();
                } else if (mouseEvent.getX() >=  660 && mouseEvent.getX() <= 695 && mouseEvent.getY() >= 50 && mouseEvent.getY() <= 85) {
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

                gc.clearRect(0, verticalMargin - 2 * Config.PREDATOR_RADIUS, world.getWidth(),  2 * Config.PREDATOR_RADIUS);
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
        if (!Config.DEBUG) {
            gc.setFill(boidColor);
        }

        for (Boid boid : world.getBoids()) {
            if (boid.isDead()) {
                if (Config.DEBUG) {
                    gc.setFill(boidDeadColor);

                    drawMovableObject(boid);
                }
            } else {
                if (Config.DEBUG) {
                    gc.setFill(boidNeighbourColor);

                    gc.setGlobalAlpha(0.1);
                    drawCircle(boid.getX(), boid.getY(), Config.NEIGHBOURHOOD_RADIUS);
                    gc.setGlobalAlpha(1.0);

                    if (boid.isAvoiding()) {
                        gc.setFill(boidAvoidingColor);
                    } else {
                        gc.setFill(boidColor);
                    }
                }

                drawMovableObject(boid);
            }
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
