package ex1;

import java.util.HashSet;
import java.util.Set;


public class Boid extends MovableWorldObject {
    private boolean avoiding = false;
    private boolean fleeing = false;

    private Set<Boid> visibleNeighbours = new HashSet<>();
    private Set<Predator> visiblePredators = new HashSet<>();


    public boolean isAvoiding () {
        return avoiding;
    }

    public void setAvoiding (boolean avoiding) {
        this.avoiding = avoiding;
    }

    public boolean isFleeing () {
        return fleeing;
    }

    public void setFleeing (boolean fleeing) {
        this.fleeing = fleeing;
    }

    public Set<Boid> getVisibleNeighbours () {
        return visibleNeighbours;
    }

    public void addVisibleNeighbour (Boid boid) {
        visibleNeighbours.add(boid);
    }

    public void removeVisibleNeighbour (Boid boid) {
        visibleNeighbours.remove(boid);
    }

    public void emptyVisibleNeighbours () {
        visibleNeighbours.clear();
    }

    public Set<Predator> getVisiblePredators () {
        return visiblePredators;
    }

    public void addVisiblePredator (Predator predator) {
        visiblePredators.add(predator);
    }

    public void removeVisiblePredator (Predator predator) {
        visiblePredators.remove(predator);
    }

    public void emptyVisiblePredators () {
        visiblePredators.clear();
    }


    public Boid(double x, double y, double radius, World world, double vX, double vY, double maxSpeed) {
        super(x, y, radius, world, vX, vY, maxSpeed);
    }

    public void clearNeighbours () {
        emptyVisibleNeighbours();
        emptyVisiblePredators();
    }

    public double[] calculateForces () {
        double[] totalForce = new double[] {0.0, 0.0};

        for (Force force : getWorld().getForces()) {
            double[] forceValue = force.calculateForce(this);

            totalForce[0] += forceValue[0] * force.getWeight();
            totalForce[1] += forceValue[1] * force.getWeight();
        }

        return totalForce;
    }
}
