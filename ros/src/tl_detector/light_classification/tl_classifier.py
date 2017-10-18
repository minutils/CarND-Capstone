from styx_msgs.msg import TrafficLight
import tensorflow as tf



class TLClassifier(object):

    def __init__(self):
        #TODO load classifier
        pass

    def open_model(self, path_to_frozen):
	detection_graph = tf.Graph()
	with detection_graph.as_default():
    		od_graph_def = tf.GraphDef()
    		with tf.gfile.GFile(path_to_frozen, 'rb') as fid:
        		serialized_graph = fid.read()
        		od_graph_def.ParseFromString(serialized_graph)
        		tf.import_graph_def(od_graph_def, name='')
	return True

    def load_image_into_numpy_array(image):
    	(im_width, im_height) = image.size
    	return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
	

    def get_classification(self, image):

        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        return TrafficLight.UNKNOWN
