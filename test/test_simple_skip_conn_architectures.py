import tensorflow as tf
import unittest

from context import fastISM


class TestSimpleSingleInMultiOutArchitectures(unittest.TestCase):
    def test_conv_add_two_fc(self):
        # inp -> C -> C-> Add -> D -> y
        #          |_______^
        inp = tf.keras.Input((100, 4))
        x = tf.keras.layers.Conv1D(20, 3)(inp)
        x1 = tf.keras.layers.Conv1D(20, 3, padding='same')(x)
        x = tf.keras.layers.Add()([x, x1])
        x = tf.keras.layers.Flatten()(x)
        y = tf.keras.layers.Dense(1)(x)
        model = tf.keras.Model(inputs=inp, outputs=y)

        fast_ism_model = fastISM.FastISM(
            model, test_correctness=False)

        self.assertTrue(fast_ism_model.test_correctness())

    def test_conv_add_three_fc(self):
        #          ^-- C---|
        # inp -> C ->  C-> Add -> D -> y
        #          |_______^
        inp = tf.keras.Input((100, 4))
        x = tf.keras.layers.Conv1D(20, 3)(inp)
        x1 = tf.keras.layers.Conv1D(20, 3, padding='same')(x)
        x2 = tf.keras.layers.Conv1D(20, 5, padding='same')(x)
        x = tf.keras.layers.Add()([x, x1, x2])
        x = tf.keras.layers.Flatten()(x)
        y = tf.keras.layers.Dense(1)(x)
        model = tf.keras.Model(inputs=inp, outputs=y)

        fast_ism_model = fastISM.FastISM(
            model, test_correctness=False)

        self.assertTrue(fast_ism_model.test_correctness())

    def test_skip_then_mxp(self):
        #          _________
        #          ^       |
        # inp -> C ->  C-> Add ->  MXP -> D -> y
        #
        inp = tf.keras.Input((100, 4))
        x = tf.keras.layers.Conv1D(20, 3)(inp)
        x1 = tf.keras.layers.Conv1D(20, 3, padding='same')(x)
        x1 = tf.keras.layers.Add()([x, x1])
        x2 = tf.keras.layers.MaxPooling1D(3)(x1)

        y = tf.keras.layers.Dense(1)(x2)
        model = tf.keras.Model(inputs=inp, outputs=y)

        fast_ism_model = fastISM.FastISM(
            model, test_correctness=False)

        self.assertTrue(fast_ism_model.test_correctness())

    def test_mini_dense_net_1(self):
        #          _________  ___________
        #          ^       |  ^         |
        # inp -> C ->  C-> Add -> C -> Add -> D -> y
        #          |____________________^
        inp = tf.keras.Input((100, 4))
        x = tf.keras.layers.Conv1D(20, 3)(inp)
        x1 = tf.keras.layers.Conv1D(20, 3, padding='same')(x)
        x1 = tf.keras.layers.Add()([x, x1])
        x2 = tf.keras.layers.Conv1D(20, 5, padding='same')(x1)
        x2 = tf.keras.layers.Add()([x, x1, x2])
        x2 = tf.keras.layers.Flatten()(x2)
        y = tf.keras.layers.Dense(1)(x2)
        model = tf.keras.Model(inputs=inp, outputs=y)

        fast_ism_model = fastISM.FastISM(
            model, test_correctness=False)

        self.assertTrue(fast_ism_model.test_correctness())

    def test_mini_dense_net_2(self):
        #          _________  ___________            _________  ___________
        #          ^       |  ^         |            ^       |  ^         |
        # inp -> C ->  C-> Add -> C -> Add -> MXP -> C -> C-> Add -> C -> Add -> D -> y        
        #          |____________________^            |____________________^
        inp = tf.keras.Input((100, 4))
        x = tf.keras.layers.Conv1D(20, 3)(inp)
        x1 = tf.keras.layers.Conv1D(20, 3, padding='same')(x)
        x1 = tf.keras.layers.Add()([x, x1])
        x2 = tf.keras.layers.Conv1D(20, 5, padding='same')(x1)
        x2 = tf.keras.layers.Add()([x, x1, x2])
        x2 = tf.keras.layers.MaxPooling1D(3)(x2)
        x2 = tf.keras.layers.Conv1D(10, 2)(x2)

        x3 = tf.keras.layers.Conv1D(10, 7, padding='same')(x2)
        x3 = tf.keras.layers.Maximum()([x2, x3])
        x4 = tf.keras.layers.Conv1D(10, 4, padding='same')(x3)
        x4 = tf.keras.layers.Add()([x2, x3, x4])

        x4 = tf.keras.layers.Flatten()(x4)
        y = tf.keras.layers.Dense(1)(x4)
        model = tf.keras.Model(inputs=inp, outputs=y)

        fast_ism_model = fastISM.FastISM(
            model, test_correctness=False)

        self.assertTrue(fast_ism_model.test_correctness())


if __name__ == '__main__':
    unittest.main()
