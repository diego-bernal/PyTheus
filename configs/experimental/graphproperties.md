# Graph Properties
This list gives properties that could be useful to look at when analyzing graph data generated by ML models.
It would make sense to implement some of them in a standardized way in Theseus. 

* number of edges
* local dimensions
* number of perfect matchings
* number of perfect matchings of bleached (uncolored) graph
* idle edges (edges not part of any PM)
* number of duplicate edges
* number of self loops
* cancellation happening
* connectedness
* vertices with degree one (obviously forced in PM)
* edges that are part of every PM (less obviously forced in PMs)

### states generated by the graph
* number of terms in generated state
* SRV
* concurrence