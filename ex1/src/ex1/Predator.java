package ex1;

import java.util.HashSet;
import java.util.Set;

public class Predator extends MovableWorldObject {
    private Set<Boid> visiblePreys = new HashSet<>();


    public Set<Boid> getVisiblePreys () {
        return visiblePreys;
    }

    public void addVisiblePrey (Boid prey) {
        visiblePreys.add(prey);
    }

    public void removeVisiblePrey (Boid prey) {
        visiblePreys.remove(prey);
    }

    public void emptyVisiblePreys () {
        visiblePreys.clear();
    }


    public Predator(double x, double y, double radius, World world, double vX, double vY, double maxSpeed) {
        super(x, y, radius, world, vX, vY, maxSpeed);
    }


    public void clearNeighbours () {
        emptyVisiblePreys();
    }

    public double[] calculateForces () {
        double[] totalForce = new double[] {0.0, 0.0};

        for (Boid prey : visiblePreys) {
            if (!prey.isDead()) {
                double weight = this.distanceWeight(prey);
                double[] direction = Maths.normalizeVector(shortestDistanceVectorToPoint(prey.getPosition()));

                totalForce[0] += weight * direction[0];
                totalForce[1] += weight * direction[1];
            }
        }

        totalForce = Maths.normalizeVector(totalForce);

        return Maths.scaleVector(totalForce, Config.CHASE_WEIGHT);
    }
}
