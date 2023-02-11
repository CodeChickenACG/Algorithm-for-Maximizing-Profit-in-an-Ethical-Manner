from collections import deque


class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info

    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """
        p = {}
        a = self.info["betas"]
        c = a.keys()
        b = self.info["bandwidths"]
        fcc = self.info["is_fcc"]

        graph_size = len(self.graph)
        priors = [-1] * graph_size
        search_queue = deque()
        search_queue.append(self.isp)
        while search_queue:
            node = search_queue.popleft()

            sorted_clients = {}
            sorted_fcc = {}
            sorted_routers = {}
            for neighbor in self.graph[node]:

                if b[neighbor] < 39:
                    b[neighbor] = 39

                if priors[neighbor] == -1 and neighbor != self.isp:
                    if (neighbor in c):
                        if fcc[neighbor] == 1:
                            sorted_fcc[neighbor] = a[neighbor]
                        else:
                            sorted_clients[neighbor] = a[neighbor]
                    else:
                        sorted_routers[neighbor] = b[neighbor]
            sorted_fcc = dict(sorted(sorted_fcc.items(), key=lambda item: item[1]))
            sorted_clients = dict(sorted(sorted_clients.items(), key=lambda item: item[1]))
            sorted_routers = dict(sorted(sorted_routers.items(), key=lambda item: item[1]))

            for n in sorted_fcc:
                if (priors[n] == -1 and n != self.isp):
                    priors[n] = node
                    search_queue.append(n)

            for n in sorted_clients:
                if (priors[n] == -1 and n != self.isp):
                    priors[n] = node
                    search_queue.append(n)

            for n in sorted_routers:
                if (priors[n] == -1 and n != self.isp):
                    priors[n] = node
                    search_queue.append(n)

        for client in self.info["list_clients"]:
            path = []
            current_node = client
            while (current_node != -1):
                path.append(current_node)
                current_node = priors[current_node]
            path = path[::-1]
            p[client] = path

        paths, bandwidths, priorities = p, b, {}
        # Note: You do not need to modify all of the above. For Problem 1,
        # only the paths variable needs to be modified. If you do modify a variable you are not supposed to,
        # you might notice different revenues outputted by the Driver locally since the autograder will ignore the
        # variables not relevant for the problem.
        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return (paths, bandwidths, priorities)