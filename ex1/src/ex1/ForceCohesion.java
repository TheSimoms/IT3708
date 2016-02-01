package ex1;

public class ForceCohesion extends Force {
    public ForceCohesion (World world, double weight) {
        super(world, weight);
    }


    public double[] calculateForce (Boid boid) {
        double[] force = new double[] {0.0, 0.0};

        if (boid.getVisibleNeighbours().size() == 0) {
            return force;
        }

        for (Boid neighbour : boid.getVisibleNeighbours()) {
            force[0] += neighbour.getX();
            force[1] += neighbour.getY();
        }

        int neighbourCount = boid.getVisibleNeighbours().size();

        force[0] /= neighbourCount;
        force[1] /= neighbourCount;

        return Maths.normalizeVector(boid.shortestDistanceVectorToPoint(force));
    }
}
