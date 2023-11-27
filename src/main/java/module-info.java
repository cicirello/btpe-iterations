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
module org.cicirello.btpe_iterations {
  exports org.cicirello.experiments.btpe;

  requires org.cicirello.rho_mu;
}
