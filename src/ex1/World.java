package ex1;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class World {
    private int width, height;

    private ArrayList<Boid> boids = new ArrayList<>();
    private ArrayList<Predator> predators = new ArrayList<>();
    private ArrayList<Obstacle> obstacles = new ArrayList<>();

    private ArrayList<Force> forces = new ArrayList<>();


    public int getWidth () {
        return width;
    }

    public void setWidth (int width) {
        this.width = width;
    }

    public int getHeight () {
        return height;
    }

    public void setHeight (int height) {
        this.height = height;
    }

    public ArrayList<Boid> getBoids () {
        return boids;
    }

    public void addBoid (Boid boid) {
        boids.add(boid);
    }

    public ArrayList<Predator> getPredators () {
        return predators;
    }

    public void addPredator (Predator predator) {
        predators.add(predator);
    }

    public void removePredators () {
        predators.clear();
    }

    public ArrayList<Obstacle> getObstacles () {
        return obstacles;
    }

    public void addObstacle (Obstacle obstacle) {
        obstacles.add(obstacle);
    }

    public void removeObstacles () {
        obstacles.clear();
    }

    public ArrayList<Force> getForces () {
        return forces;
    }

    public void setForces (ArrayList<Force> forces) {
        this.forces = forces;
    }

    public void addForce (Force force) {
        forces.add(force);
    }

    public World (int width, int height) {
        this.width = width;
        this.height = height;
    }

    public ArrayList<WorldObject> getObjects () {
        ArrayList<WorldObject> res = new ArrayList<>();

        res.addAll(boids);
        res.addAll(predators);
        res.addAll(obstacles);

        return res;
    }

    public ArrayList<MovableWorldObject> getMovableObjects () {
        ArrayList<MovableWorldObject> res = new ArrayList<>();

        res.addAll(boids);
        res.addAll(predators);

        return res;
    }

    public boolean isPositionOccupied (int[] position) {
        for (WorldObject object : getObjects()) {
            if (Arrays.equals(object.getPosition(), position)) {
                return true;
            }
        }

        return false;
    }

    public int[] generateRandomCoordinates () {
        int[] coordinates;

        do {
            coordinates = new int[] {(int)(Math.random() * width), (int)(Math.random() * height)};
        } while (isPositionOccupied(coordinates));

        return coordinates;
    }

    public double generateRandomSpeed (double maxSpeed) {
        return (-1.0 + 2 * Math.random() * maxSpeed);
    }

    public double[] generateRandomVelocity (double maxSpeed) {
        return new double[] {generateRandomSpeed(maxSpeed), generateRandomSpeed(maxSpeed)};
    }

    public void addRandomBoids (int n) {
        int remainingBoids = n;

        while (remainingBoids > 0) {
            int[] coordinates = generateRandomCoordinates();
            double[] velocity = generateRandomVelocity(Config.BOID_MAX_SPEED);

            boids.add(new Boid(coordinates[0], coordinates[1], Config.BOID_RADIUS, this, velocity[0], velocity[1], Config.BOID_MAX_SPEED));

            remainingBoids--;
        }
    }

    public void addRandomPredator () {
        int[] coordinates = generateRandomCoordinates();
        double[] velocity = generateRandomVelocity(Config.PREDATOR_MAX_SPEED);

        predators.add(new Predator(coordinates[0], coordinates[1], Config.PREDATOR_RADIUS, this, velocity[0], velocity[1], Config.PREDATOR_MAX_SPEED));
    }

    public void addRandomObstacle() {
        int[] coordinates = generateRandomCoordinates();

        obstacles.add(new Obstacle(coordinates[0], coordinates[1], Config.OBSTACLE_RADIUS, this));
    }

    public void addObstacle(int[] position, double radius) {
        obstacles.add(new Obstacle(position[0], position[1], radius, this));
    }

    public int[] getDimensons () {
        return new int[] {width, height};
    }

    public double[] calculateForces (Boid boid) {
        double[] totalForce = new double[] {0.0, 0.0};

        for (Force force : forces) {
            double[] forceValue = force.calculateForce(boid);

            totalForce[0] += forceValue[0] * force.getWeight();
            totalForce[1] += forceValue[1] * force.getWeight();
        }

        return totalForce;
    }

    public void updateObjectMoves () {
        for (MovableWorldObject object : getMovableObjects()) {
            if (!object.isDead()) {
                object.updateVelocity();
                object.limitVelocity();
                object.updateNextPosition();
            }
        }
    }

    public void performMoves () {
        for (MovableWorldObject object : getMovableObjects()) {
            object.performMove();
        }
    }

    public void reviveBoids () {
        for (Boid boid : boids) {
            boid.setDead(false);
        }
    }

    public void setDistance (MovableWorldObject object0, MovableWorldObject object1, double distance) {
        object0.setDistance(object1, distance);
        object1.setDistance(object0, distance);
    }

    public void clearNeighbourLists () {
        for (Boid boid : boids) {
            boid.getVisibleNeighbours().clear();
            boid.getVisiblePredators().clear();
        }

        for (Predator predator : predators) {
            predator.getVisiblePreys().clear();
        }
    }

    public void updateNeighbourLists () {
        clearNeighbourLists();

        Set<Boid> finishedBoids = new HashSet<>();

        for (Boid boid : boids) {
            finishedBoids.add(boid);

            if (boid.isDead()) {
                continue;
            }

            for (Boid neighbour : boids) {
                if (finishedBoids.contains(neighbour) || neighbour.isDead()) {
                    continue;
                }

                double distance = boid.getDistanceToObject(neighbour);

                if (distance < Config.NEIGHBOURHOOD_RADIUS) {
                    boid.addVisibleNeighbour(neighbour);
                    neighbour.addVisibleNeighbour(boid);

                    setDistance(boid, neighbour, distance);
                }
            }

            for (Predator predator : predators) {
                double distance = boid.getDistanceToObject(predator);

                if (distance < Config.NEIGHBOURHOOD_RADIUS) {
                    boid.addVisiblePredator(predator);
                    predator.addVisiblePrey(boid);

                    setDistance(boid, predator, distance);
                }
            }
        }
    }
}
