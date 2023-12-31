import paddle
import unittest
import sys
from reco_encoder.data.input_layer import UserItemRecDataProvider
from reco_encoder.model.model import AutoEncoder, MSEloss

sys.path.append("data")
sys.path.append("model")


class iRecAutoEncoderTest(unittest.TestCase):
    def test_CPU(self):
        print("iRecAutoEncoderTest Test on  CPU started")
        params = {}
        params["batch_size"] = 64
        params["data_dir"] = "test/testData_iRec"
        data_layer = UserItemRecDataProvider(params=params)
        print("Vector dim: {}".format(data_layer.vector_dim))
        print("Total items found: {}".format(len(data_layer.data.keys())))
        self.assertTrue(len(data_layer.data.keys()) > 0)
        encoder = AutoEncoder(
            layer_sizes=[data_layer.vector_dim, 256, 128], is_constrained=True
        )
        print(encoder)
        print(encoder.parameters())
        optimizer = paddle.optimizer.SGD(
            learning_rate=0.01, parameters=encoder.parameters(), momentum=0.9
        )
        for epoch in range(20):
            for i, mb in enumerate(data_layer.iterate_one_epoch()):
                inputs = mb.to_dense()
                optimizer.clear_grad()
                outputs = encoder(inputs)
                loss, num_ratings = MSEloss(outputs, inputs)
                loss = loss / num_ratings
                loss.backward()
                optimizer.step()
                print("[%d, %5d] loss: %.7f" % (epoch, i, loss.item()))

    def test_GPU(self):
        print("iRecAutoEncoderTest Test on GPU started")
        params = {}
        params["batch_size"] = 32
        params["data_dir"] = "test/testData_iRec"
        data_layer = UserItemRecDataProvider(params=params)
        print("Total items found: {}".format(len(data_layer.data.keys())))
        self.assertTrue(len(data_layer.data.keys()) > 0)
        encoder = AutoEncoder(
            layer_sizes=[data_layer.vector_dim, 1024, 512, 512, 512, 512, 128]
        )
        encoder
        optimizer = paddle.optimizer.Adam(
            parameters=encoder.parameters(), weight_decay=0.0
        )
        print(encoder)
        for epoch in range(30):
            total_epoch_loss = 0.0
            denom = 0.0
            for i, mb in enumerate(data_layer.iterate_one_epoch()):
                inputs = mb.to_dense()
                optimizer.clear_grad()
                outputs = encoder(inputs)
                loss, num_ratings = MSEloss(outputs, inputs)
                loss = loss / num_ratings
                loss.backward()
                optimizer.step()
                total_epoch_loss += loss.item()
                denom += 1
            print("Total epoch {} loss: {}".format(epoch, total_epoch_loss / denom))


class uRecAutoEncoderTest(unittest.TestCase):
    def test_CPU(self):
        print("uRecAutoEncoderTest Test on  CPU started")
        params = {}
        params["batch_size"] = 256
        params["data_dir"] = "test/testData_uRec"
        data_layer = UserItemRecDataProvider(params=params)
        print("Vector dim: {}".format(data_layer.vector_dim))
        print("Total items found: {}".format(len(data_layer.data.keys())))
        self.assertTrue(len(data_layer.data.keys()) > 0)
        encoder = AutoEncoder(
            layer_sizes=[data_layer.vector_dim, 128, data_layer.vector_dim]
        )
        optimizer = paddle.optimizer.SGD(
            learning_rate=0.01, parameters=encoder.parameters(), momentum=0.9
        )
        for epoch in range(1):
            for i, mb in enumerate(data_layer.iterate_one_epoch()):
                inputs = mb.to_dense()
                optimizer.clear_grad()
                outputs = encoder(inputs)
                loss, num_ratings = MSEloss(outputs, inputs)
                loss = loss / num_ratings
                loss.backward()
                optimizer.step()
                print("[%d, %5d] loss: %.7f" % (epoch, i, loss.item()))
                if i == 5:
                    break

    def test_GPU(self):
        print("uRecAutoEncoderTest Test on GPU started")
        params = {}
        params["batch_size"] = 64
        params["data_dir"] = "test/testData_uRec"
        data_layer = UserItemRecDataProvider(params=params)
        print("Total items found: {}".format(len(data_layer.data.keys())))
        self.assertTrue(len(data_layer.data.keys()) > 0)
        encoder = AutoEncoder(layer_sizes=[data_layer.vector_dim, 1024, 512, 512, 128])
        encoder
        optimizer = paddle.optimizer.Adam(
            parameters=encoder.parameters(), weight_decay=0.0
        )
        print(encoder)
        for epoch in range(2):
            total_epoch_loss = 0.0
            denom = 0.0
            for i, mb in enumerate(data_layer.iterate_one_epoch()):
                inputs = mb.to_dense()
                optimizer.clear_grad()
                outputs = encoder(inputs)
                loss, num_ratings = MSEloss(outputs, inputs)
                loss = loss / num_ratings
                loss.backward()
                optimizer.step()
                total_epoch_loss += loss.item()
                denom += 1
            print("Total epoch {} loss: {}".format(epoch, total_epoch_loss / denom))


if __name__ == "__main__":
    unittest.main()
