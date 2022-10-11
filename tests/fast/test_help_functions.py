import unittest
from tokenize import String

from theseus.fancy_classes import State
from theseus.help_functions import readableState, prepEdgeList, removeConnections, makeUnicolor, flatten_lists, \
    get_all_kets_for_given_dim, makeState, stringToTerm
from theseus.main import run_main, read_config


class TestHelpFunctionsModule(unittest.TestCase):

    def test_readableState(self):
        term_list = ['000000', '111000', '222000', '333000']
        target_state = State(term_list, imaginary=False)
        expected = {'|000000>': True, '|111000>': True, '|222000>': True, '|333000>': True}
        self.assertEqual(expected, readableState(target_state))

    def test_flattenlistwithstrings(self):
        expected_list = ['a', 'b', 'c']
        flattenlist = flatten_lists(expected_list)
        self.assertListEqual(expected_list, flattenlist)

    def test_flattenlistwithnumbers(self):
        expected_lists = list(range(1, 101))
        flattenlist = flatten_lists([expected_lists])
        self.assertListEqual([expected_lists], [flattenlist])

    def test_removeConnections(self):
        edge_list = [(0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1), (0, 2, 0, 0), (0, 2, 0, 1), (0, 2, 1, 0),
                     (0, 2, 1, 1), (0, 3, 0, 0), (0, 3, 0, 1), (0, 3, 1, 0), (0, 3, 1, 1), (0, 4, 0, 0), (0, 4, 1, 0),
                     (0, 5, 0, 0), (0, 5, 1, 0), (1, 2, 0, 0), (1, 2, 0, 1), (1, 2, 1, 0), (1, 2, 1, 1), (1, 3, 0, 0),
                     (1, 3, 0, 1), (1, 3, 1, 0), (1, 3, 1, 1), (1, 4, 0, 0), (1, 4, 1, 0), (1, 5, 0, 0), (1, 5, 1, 0),
                     (2, 3, 0, 0), (2, 3, 0, 1), (2, 3, 1, 0), (2, 3, 1, 1), (2, 4, 0, 0), (2, 4, 1, 0), (2, 5, 0, 0),
                     (2, 5, 1, 0), (3, 4, 0, 0), (3, 4, 1, 0), (3, 5, 0, 0), (3, 5, 1, 0), (4, 5, 0, 0)]
        connect_list = [[0, 1]]
        expected_edge_list = [(0, 2, 0, 0), (0, 2, 0, 1), (0, 2, 1, 0), (0, 2, 1, 1), (0, 3, 0, 0), (0, 3, 0, 1),
                              (0, 3, 1, 0), (0, 3, 1, 1), (0, 4, 0, 0), (0, 4, 1, 0), (0, 5, 0, 0), (0, 5, 1, 0),
                              (1, 2, 0, 0), (1, 2, 0, 1), (1, 2, 1, 0), (1, 2, 1, 1), (1, 3, 0, 0), (1, 3, 0, 1),
                              (1, 3, 1, 0), (1, 3, 1, 1), (1, 4, 0, 0), (1, 4, 1, 0), (1, 5, 0, 0), (1, 5, 1, 0),
                              (2, 3, 0, 0), (2, 3, 0, 1), (2, 3, 1, 0), (2, 3, 1, 1), (2, 4, 0, 0), (2, 4, 1, 0),
                              (2, 5, 0, 0), (2, 5, 1, 0), (3, 4, 0, 0), (3, 4, 1, 0), (3, 5, 0, 0), (3, 5, 1, 0),
                              (4, 5, 0, 0)]
        actual_edgelist = removeConnections(edge_list, connect_list)
        self.assertEqual(expected_edge_list, actual_edgelist)

    def test_prepEdgelist(self):
        edge_list = [(0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 0, 3), (0, 1, 1, 0), (0, 1, 1, 1), (0, 1, 1, 2),
                     (0, 1, 1, 3), (0, 1, 2, 0), (0, 1, 2, 1), (0, 1, 2, 2), (0, 1, 2, 3), (0, 1, 3, 0), (0, 1, 3, 1),
                     (0, 1, 3, 2), (0, 1, 3, 3), (0, 2, 0, 0), (0, 2, 0, 1), (0, 2, 0, 2), (0, 2, 0, 3), (0, 2, 1, 0),
                     (0, 2, 1, 1), (0, 2, 1, 2), (0, 2, 1, 3), (0, 2, 2, 0), (0, 2, 2, 1), (0, 2, 2, 2), (0, 2, 2, 3),
                     (0, 2, 3, 0), (0, 2, 3, 1), (0, 2, 3, 2), (0, 2, 3, 3), (0, 3, 0, 0), (0, 3, 1, 0), (0, 3, 2, 0),
                     (0, 3, 3, 0), (0, 4, 0, 0), (0, 4, 1, 0), (0, 4, 2, 0), (0, 4, 3, 0), (0, 5, 0, 0), (0, 5, 1, 0),
                     (0, 5, 2, 0), (0, 5, 3, 0), (1, 2, 0, 0), (1, 2, 0, 1), (1, 2, 0, 2), (1, 2, 0, 3), (1, 2, 1, 0),
                     (1, 2, 1, 1), (1, 2, 1, 2), (1, 2, 1, 3), (1, 2, 2, 0), (1, 2, 2, 1), (1, 2, 2, 2), (1, 2, 2, 3),
                     (1, 2, 3, 0), (1, 2, 3, 1), (1, 2, 3, 2), (1, 2, 3, 3), (1, 3, 0, 0), (1, 3, 1, 0), (1, 3, 2, 0),
                     (1, 3, 3, 0), (1, 4, 0, 0), (1, 4, 1, 0), (1, 4, 2, 0), (1, 4, 3, 0), (1, 5, 0, 0), (1, 5, 1, 0),
                     (1, 5, 2, 0), (1, 5, 3, 0), (2, 3, 0, 0), (2, 3, 1, 0), (2, 3, 2, 0), (2, 3, 3, 0), (2, 4, 0, 0),
                     (2, 4, 1, 0), (2, 4, 2, 0), (2, 4, 3, 0), (2, 5, 0, 0), (2, 5, 1, 0), (2, 5, 2, 0), (2, 5, 3, 0),
                     (3, 4, 0, 0), (3, 5, 0, 0), (4, 5, 0, 0)]


        config = {'bulk_thr': 0.01, 'edges_tried': 20, 'foldername': 'ghz_346', 'ftol': 1e-06, 'loss_func': 'cr',
                  'num_anc': 3, 'num_pre': 1, 'optimizer': 'L-BFGS-B', 'imaginary': False, 'safe_hist': True,
                  'samples': 1, 'target_state': ['000', '111', '222', '333'], 'thresholds': [0.25, 0.1],
                  'tries_per_edge': 5, 'unicolor': False}

        expected_edge_list = [(0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 0, 3), (0, 1, 1, 0), (0, 1, 1, 1),
                              (0, 1, 1, 2), (0, 1, 1, 3), (0, 1, 2, 0), (0, 1, 2, 1), (0, 1, 2, 2), (0, 1, 2, 3),
                              (0, 1, 3, 0), (0, 1, 3, 1), (0, 1, 3, 2), (0, 1, 3, 3), (0, 2, 0, 0), (0, 2, 0, 1),
                              (0, 2, 0, 2), (0, 2, 0, 3), (0, 2, 1, 0), (0, 2, 1, 1), (0, 2, 1, 2), (0, 2, 1, 3),
                              (0, 2, 2, 0), (0, 2, 2, 1), (0, 2, 2, 2), (0, 2, 2, 3), (0, 2, 3, 0), (0, 2, 3, 1),
                              (0, 2, 3, 2), (0, 2, 3, 3), (0, 3, 0, 0), (0, 3, 1, 0), (0, 3, 2, 0), (0, 3, 3, 0),
                              (0, 4, 0, 0), (0, 4, 1, 0), (0, 4, 2, 0), (0, 4, 3, 0), (0, 5, 0, 0), (0, 5, 1, 0),
                              (0, 5, 2, 0), (0, 5, 3, 0), (1, 2, 0, 0), (1, 2, 0, 1), (1, 2, 0, 2), (1, 2, 0, 3),
                              (1, 2, 1, 0), (1, 2, 1, 1), (1, 2, 1, 2), (1, 2, 1, 3), (1, 2, 2, 0), (1, 2, 2, 1),
                              (1, 2, 2, 2), (1, 2, 2, 3), (1, 2, 3, 0), (1, 2, 3, 1), (1, 2, 3, 2), (1, 2, 3, 3),
                              (1, 3, 0, 0), (1, 3, 1, 0), (1, 3, 2, 0), (1, 3, 3, 0), (1, 4, 0, 0), (1, 4, 1, 0),
                              (1, 4, 2, 0), (1, 4, 3, 0), (1, 5, 0, 0), (1, 5, 1, 0), (1, 5, 2, 0), (1, 5, 3, 0),
                              (2, 3, 0, 0), (2, 3, 1, 0), (2, 3, 2, 0), (2, 3, 3, 0), (2, 4, 0, 0), (2, 4, 1, 0),
                              (2, 4, 2, 0), (2, 4, 3, 0), (2, 5, 0, 0), (2, 5, 1, 0), (2, 5, 2, 0), (2, 5, 3, 0),
                              (3, 4, 0, 0), (3, 5, 0, 0), (4, 5, 0, 0)]

        actual_edge_list = prepEdgeList(edge_list, config)

        self.assertEqual(expected_edge_list, actual_edge_list)


    def test_makeUnicolor(self):
        temporary_string = [(0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 0, 3), (0, 1, 1, 0), (0, 1, 1, 1), (0, 1, 1, 2),
                            (0, 1, 1, 3), (0, 1, 2, 0), (0, 1, 2, 1), (0, 1, 2, 2), (0, 1, 2, 3), (0, 1, 3, 0), (0, 1, 3, 1),
                            (0, 1, 3, 2), (0, 1, 3, 3), (0, 2, 0, 0), (0, 2, 0, 1), (0, 2, 0, 2), (0, 2, 0, 3), (0, 2, 1, 0),
                            (0, 2, 1, 1), (0, 2, 1, 2), (0, 2, 1, 3), (0, 2, 2, 0), (0, 2, 2, 1), (0, 2, 2, 2), (0, 2, 2, 3),
                            (0, 2, 3, 0), (0, 2, 3, 1), (0, 2, 3, 2), (0, 2, 3, 3), (0, 3, 0, 0), (0, 3, 1, 0), (0, 3, 2, 0),
                            (0, 3, 3, 0), (0, 4, 0, 0), (0, 4, 1, 0), (0, 4, 2, 0), (0, 4, 3, 0), (0, 5, 0, 0), (0, 5, 1, 0),
                            (0, 5, 2, 0), (0, 5, 3, 0), (1, 2, 0, 0), (1, 2, 0, 1), (1, 2, 0, 2), (1, 2, 0, 3), (1, 2, 1, 0),
                            (1, 2, 1, 1), (1, 2, 1, 2), (1, 2, 1, 3), (1, 2, 2, 0), (1, 2, 2, 1), (1, 2, 2, 2), (1, 2, 2, 3),
                            (1, 2, 3, 0), (1, 2, 3, 1), (1, 2, 3, 2), (1, 2, 3, 3), (1, 3, 0, 0), (1, 3, 1, 0), (1, 3, 2, 0),
                            (1, 3, 3, 0), (1, 4, 0, 0), (1, 4, 1, 0), (1, 4, 2, 0), (1, 4, 3, 0), (1, 5, 0, 0), (1, 5, 1, 0),
                            (1, 5, 2, 0), (1, 5, 3, 0), (2, 3, 0, 0), (2, 3, 1, 0), (2, 3, 2, 0), (2, 3, 3, 0), (2, 4, 0, 0),
                            (2, 4, 1, 0), (2, 4, 2, 0), (2, 4, 3, 0), (2, 5, 0, 0), (2, 5, 1, 0), (2, 5, 2, 0), (2, 5, 3, 0),
                            (3, 4, 0, 0), (3, 5, 0, 0), (4, 5, 0, 0)]
        expected_sorted_edge = [(0, 1, 0, 0), (0, 1, 1, 1), (0, 1, 2, 2), (0, 1, 3, 3), (0, 2, 0, 0), (0, 2, 1, 1),
                                (0, 2, 2, 2), (0, 2, 3, 3), (0, 3, 0, 0), (0, 4, 0, 0), (0, 5, 0, 0), (1, 2, 0, 0),
                                (1, 2, 1, 1), (1, 2, 2, 2), (1, 2, 3, 3), (1, 3, 0, 0), (1, 4, 0, 0), (1, 5, 0, 0),
                                (2, 3, 0, 0), (2, 4, 0, 0), (2, 5, 0, 0), (3, 4, 0, 0), (3, 5, 0, 0), (4, 5, 0, 0)]
        temp_node = 6
        out_partition = makeUnicolor(temporary_string, temp_node)
        self.assertEqual(expected_sorted_edge, out_partition)

        pass

    def test_get_all_kets_for_given_dim(self):
        actual = get_all_kets_for_given_dim([2, 2, 2, 2])
        print(len(actual))
        self.assertEqual(16,len(actual))
        self.assertEqual([0, 1, 10, 11, 100, 101, 110, 111, 1000, 1001, 1010, 1011, 1100, 1101, 1110, 1111], actual)

    def test_makeState(self):
        actual = makeState("0000+1111+2222")
        print(actual)
        expected = [((0, 0), (1, 0), (2, 0), (3, 0)), ((0, 1), (1, 1), (2, 1), (3, 1)), ((0, 2), (1, 2), (2, 2), (3, 2))]
        self.assertEqual(expected,actual)

    def test_stringToTerm(self):
        actual = stringToTerm("0210")
        self.assertEqual(((0, 0), (1, 2), (2, 1), (3, 0)), actual)