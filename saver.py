# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 17:15:59 2022

@author: janpe
"""

from fancy_classes import Graph
import config as confi
import numpy as np
from pathlib import Path
import json


def read_json(abspath: Path) -> dict:
    """
    return the dictonary for a given abspath that is a json file

    """
    with abspath.open('r', encoding="UTF-8") as openfile:
        # Reading from json file
        dictonary = json.load(openfile)
        openfile.close()

    return dictonary


def write_json(abspath: Path, dictionary: dict) -> None:
    """
    getting an Path object and a dictonary then write the dictionary
    in a json file for the given path

    """

    # Serializing json
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    if not isinstance(abspath, Path):
        abspath = Path(abspath)

    # convert json object
    json_object = json.dumps(dictionary, cls=NumpyEncoder,
                             ensure_ascii=False, indent=4)

    ### write json to new folder ###
    # make json ending
    abspath_save = str(abspath)
    if not abspath_save.endswith('.json'):
        abspath_save += '.json'
    # check if same state exists
    counter = 0
    while Path(abspath_save).exists():
        abspath_save = str(abspath) + f'({counter})' + '.json'
        counter += 1

    abspath = Path(abspath_save)
    with abspath.open("w+", encoding="UTF-8") as file:
        file.write(json_object)
        file.close()


class saver:

    def __init__(self):
        self.summary = {item: getattr(confi, item) for item in dir(confi)
                        if not item.startswith("__") and not item.endswith("__")}
        self.best_state = None
        self.safe_path = self.get_and_create_safe_directory()
        self.best_graph = None

    def get_folder_name(self) -> str:
        """
        return the folder name: dimension of the system or confi

        """
        if confi.foldername is None:
            return '(' + '-'.join([str(w) for w in confi.dimensions]) + ')'
        else:
            return confi.foldername

    def get_and_create_safe_directory(self):
        """
        look if folder ~/data/(2-2-2-2) exists otherwise creates it
        when exists it looks if config files are the same then our
        safe directory is ~/data/(2-2-2-2) otherwise: we chose
        ~/data/(2-2-2-2)(x) for a x where the summary files are matching
        or a new directory
        """
        folder_name = self.get_folder_name()

        i = 0
        while True:  # iterate as long as one could find a proper safe folder
            pt = Path(__file__).resolve().parents[0]  # main directory
            pt = pt / 'data' / folder_name  # move data directory
            pt.mkdir(parents=True, exist_ok=True)
            summary_path = pt / 'summary.json'
            if summary_path.exists():
                if self.check_if_summary_is_same(summary_path):
                    self.foldername = folder_name
                    return pt
                else:  # adapt folder name to avoid same folder with different summarys
                    folder_name = self.get_folder_name() + f' ({i})'
                    i += 1
            else:
                self.foldername = folder_name
                write_json(pt / 'summary.json', self.summary)
                return pt

    def check_if_summary_is_same(self, path_exst_summary: Path) -> bool:
        """
        just checks if the existing summary and the current have the
        same parameters, the compare function is needed for
        distinguishing iterable and non iterables
        """

        def compare(obj_a, obj_b):
            try:
                __ = iter(obj_a)
                return all([a == b for a, b in zip(obj_a, obj_b)])
            except TypeError:
                return obj_a == obj_b

        existing_summary = read_json(path_exst_summary)
        return all([compare(self.summary[key], existing_summary[key])
                    for key in self.summary.keys()])

    def convert_graph_keys_in_str(self, graph: dict) -> dict:
        """
        here we can convert our Graph dict in a dict that has strings as keys
        we need this to save it in json file

        """
        # convert keys in str
        ret_dict = {}
        for key in graph.keys():
            if type(key) is not str:
                try:
                    ret_dict[str(key)] = graph[key]
                except:
                    try:
                        ret_dict[repr(key)] = graph[key]
                    except:
                        pass

        return ret_dict

    def safe_graph(self, topo: object) -> None:
        """
        we use an object from the class topological_opti to safe all
        infos: - the optimized graph
               - corrospoding loss
               - if confi.safe_hist is True we also safe the loss during
                 each deletion and the corosponding graph

        """

        last_lost = topo.loss_val
        abs_path = self.safe_path / self.get_file_name(topo.graph, last_lost)
        # update best graph
        if self.best_graph is None or last_lost < self.best_graph.loss_val:
            self.best_graph = topo

        safe_dic = {'graph': self.convert_graph_keys_in_str(topo.graph.graph),
                    'loss': topo.loss_val}

        try:
            safe_dic['graph_hist'] = [self.convert_graph_keys_in_str(xx.graph)
                                      for xx in topo.graph_hist]
            safe_dic['loss_hist'] = topo.loss_hist
        except AttributeError:
            pass
        write_json(abs_path, safe_dic)

    def get_file_name(self, graph: Graph, loss: float) -> str:
        """
        takes as input object Graph and generate a file name out of it

        """

        file_name = str(len(graph.graph)) + '-'
        file_name += str(len(graph.state_catalog)) + '-'

        file_name += f'{loss:.4f} '
        return file_name



