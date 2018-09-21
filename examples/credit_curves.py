# encoding: utf-8

# (c) 2017-2018 Open Risk, all rights reserved
#
# TransitionMatrix is licensed under the Apache 2.0 license a copy of which is included
# in the source distribution of TransitionMatrix. This is notwithstanding any licenses of
# third-party software included in this distribution. You may not use this file except in
# compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.


""" Compute and Visuzalize credit curves

"""

import matplotlib.pyplot as plt
from matplotlib import collections as mc

import transitionMatrix as tm
from datasets import Generic

# Initialize a single period transition matrix
# Generic is a Typical Credit Rating Transition Matrix with sever rating states and one absorbing (Default) state

M = tm.TransitionMatrix(values=Generic)

# The size of the rating scale
Ratings = M.dimension

# The Default (absorbing state)
Default = Ratings - 1


# Lets extend the matrix into ten periods (assume they represent annual intervals)
# We do this using the power method
Periods = 10
T = tm.TransitionMatrixSet(values=M, periods=Periods, method='Power', temporal_type='Cumulative')

# Lets take a look at what we have created
T.print()

# Now lets compute the default curves
# We do this one initial rating state at a time

# For example for the best rating (least likely to default) we obtain
incremental_PD, cumulative_PD, hazard_Rate, survival_Rate = T.default_curves(0)

# Now lets plot a collection of curves for all ratings

curves = []
periods = range(0, Periods)

for ri in range(0, Ratings-1):
    print("RI: ", ri)
    iPD, cPD, hR, sR = T.default_curves(ri)
    # for k in range(0, Periods):
    #     value = cPD[k]
    #     line = [(k, value), (k + 1.0, value)]
    curves.append(cPD)

fig, ax = plt.subplots()
for ri in range(0, Ratings-1):
    ax.plot(periods, curves[ri], label="RI=%d"%(ri,))

ax.autoscale()
ax.margins(0.1)
ax.set_xlabel("Periods")
ax.set_ylabel("Cumulative Default Probability")
ax.grid(True)
plt.title("Credit Curves of Generic Transition Matrix")

leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)

plt.savefig("credit_curves.png")