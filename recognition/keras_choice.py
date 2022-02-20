# -*-coding:utf-8-*-
import matplotlib.pyplot as plt
from keras import models
from keras.models import Sequential
from keras.layers import Dense, Activation
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
from keras.callbacks import TensorBoard
# os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error
# os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
tBatchSize = 100
model = models.Sequential()
model1 = Sequential()  # 顺序模型
model.add(Dense(input_dim=28 * 28, output_dim=500))
model.add(Activation('sigmoid'))
model.add(Dense(output_dim=500))
model.add(Activation('sigmoid'))
model.add(Dense(output_dim=10))
model.add(Activation('softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy', metrics=['accuracy'])
mnist = input_data.read_data_sets("emnist/", one_hot=True)

x_train, y_train = mnist.train.images, mnist.train.labels
x_test, y_test = mnist.test.images, mnist.test.labels
print(str(x_train.shape)+''+str(y_train.shape) +
      ''+str(x_test.shape)+''+str(y_test.shape))
X_train = x_train
X_test = x_test
Y_train = y_train
Y_test = y_test

history = model.fit(X_train, Y_train, batch_size=tBatchSize, epochs=20,
                    shuffle=True, verbose=0, validation_split=0.3,
                    callbacks=[TensorBoard(log_dir='mytensorboard',
                                           histogram_freq=0,
                                           write_graph=True,
                                           write_images=True)])
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('harbor-model-accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.tight_layout()
plt.savefig('./accuracyVSepoch.png')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('harbor-model-loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.tight_layout()
plt.savefig('./lossVSepoch.png')
plt.show()

model.save_weights('xuehao_keras_weight.h5')

'''第五步：输出'''
print("test set")
# 误差评价 ：按batch计算在batch用到的输入数据上模型的误差
scores = model.evaluate(X_test, Y_test, batch_size=tBatchSize, verbose=0)
print("The test loss is" + str(scores[0]))

# 根据模型获取预测结果  为了节约计算内存，也是分组（batch）load到内存中的，
result = model.predict(X_test, batch_size=tBatchSize, verbose=1)

# 找到每行最大的序号
# axis=1表示按行 取最大值   如果axis=0表示按列 取最大值 axis=None表示全部
result_max = np.argmax(result, axis=1)
# 这是结果的真实序号
test_max = np.argmax(Y_test, axis=1)


result_bool = np.equal(result_max, test_max)  # 预测结果和真实结果一致的为真（按元素比较）
true_num = np.sum(result_bool)  # 正确结果的数量
print("The accuracy of the model is " +
      str((true_num/len(result_bool))))  # 验证结果的准确率
