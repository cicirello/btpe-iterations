/*
 * An Analysis of an Open Source Binomial Random Variate Generation Algorithm.
 * Copyright (C) 2023 Vincent A. Cicirello
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

package org.cicirello.experiments.btpe;

import java.util.ArrayList;
import java.util.SplittableRandom;
import java.util.random.RandomGenerator;
import org.cicirello.math.rand.RandomVariates;

/**
 * Code to reproduce the experiments from the following article:
 *
 * <p>Vincent A. Cicirello. 2023. <a
 * href="https://www.cicirello.org/publications/engproc-56-00086.pdf">An Analysis of an Open Source
 * Binomial Random Variate Generation Algorithm</a>. <i>Engineering Proceedings</i>, 56(1), Article
 * 86, October 2023. doi:<a
 * href="https://doi.org/10.3390/ASEC2023-15349">10.3390/ASEC2023-15349</a>.
 *
 * @author <a href=https://www.cicirello.org/ target=_top>Vincent A. Cicirello</a>, <a
 *     href=https://www.cicirello.org/ target=_top>https://www.cicirello.org/</a>
 */
public final class CountIterationsBTPE {

  /**
   * Runs experiment.
   *
   * @param args ignored, no command line arguments.
   */
  public static void main(String[] args) {
    final int TRIALS = 10000;
    final int MIN_N = 32;
    final int MAX_N = 1048576;

    CallCounterBTPE generator = new CallCounterBTPE(42);

    for (int n = MIN_N; n <= MAX_N; n *= 2) {
      double[] pValues = pValuesToTest(n);
      for (double p : pValues) {
        int[] samples = new int[TRIALS];
        for (int i = 0; i < TRIALS; i++) {
          generator.reset();
          RandomVariates.nextBinomial(n, p, generator);
          samples[i] = generator.count();
        }
        System.out.println("Case " + n + " " + p);
        for (int x : samples) {
          System.out.print(x);
          System.out.print(" ");
        }
        System.out.println();
      }
    }
  }

  private static double[] pValuesToTest(int n) {
    ArrayList<Double> values = new ArrayList<Double>();

    double minRelevant = 10.0 / n;

    values.add(minRelevant);
    for (double p = 16.0 / n; p < 0.500001; p *= 2) {
      values.add(p);
    }
    for (int i = values.size() - 2; i >= 0; i--) {
      values.add(1.0 - values.get(i));
    }

    double[] result = new double[values.size()];
    for (int i = 0; i < result.length; i++) {
      result[i] = values.get(i);
    }
    return result;
  }

  /** Wraps a RandomGenerator to count the calls to nextDouble(). */
  private static class CallCounterBTPE implements RandomGenerator {

    private final RandomGenerator counter;
    private int count;

    private CallCounterBTPE(long seed) {
      counter = new SplittableRandom(seed);
      count = 0;
    }

    @Override
    public double nextDouble() {
      count++;
      return counter.nextDouble();
    }

    @Override
    public double nextDouble(double bound) {
      count++;
      return counter.nextDouble(bound);
    }

    @Override
    public long nextLong() {
      return counter.nextLong();
    }

    private void reset() {
      count = 0;
    }

    private int count() {
      return count;
    }
  }
}
