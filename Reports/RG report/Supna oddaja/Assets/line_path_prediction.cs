using System.Collections;
using System.Collections.Generic;
using System.Net;//to 
using System.IO;//to
using System; 
using UnityEngine;


// [System.Serializable]
// public class CarStateJson
// {
//     public string brake;
//     public bool gear_immediate;
//     public bool handbrake;
//     public bool is_manual_gear;
//     public int manual_gear;
//     public float steering;
//     public float throttle;
// }


namespace HttpClientEx {
	public class line_path_prediction : MonoBehaviour
	{
		LineRenderer lr;
		public GameObject car_obj;
		public Transform car_position;
		public Transform mid_path_position;
		public Transform end_path_position;
		public Vector3 a = new Vector3(5.0f, 0.0f, 0.0f);
		public Vector3 b = new Vector3(5.0f, 0.0f, 0.0f);


	    void Start() {
	        lr = GetComponent<LineRenderer>();
	        lr.positionCount = 3;
	    	lr.SetPosition(0, car_position.position);
	    	lr.SetPosition(1, mid_path_position.position);
	        lr.SetPosition(2, end_path_position.position);
	    }


	    void Update()
	    {
    		Vector3 rotation_vec = car_obj.transform.rotation.eulerAngles;


    		HttpWebRequest request = (HttpWebRequest)WebRequest.Create(@"http://127.0.0.1:5000/hub/getControl");
    		string response_string;
    		float parsed_throttle;

	        try
	        {
	            using(HttpWebResponse response = (HttpWebResponse)request.GetResponse())
	            using(Stream stream = response.GetResponseStream())
	            using(StreamReader reader = new StreamReader(stream))
	            {
	                response_string = reader.ReadToEnd();
	                CarStateJson state = (CarStateJson)JsonUtility.FromJson(response_string, typeof(CarStateJson));
	                Debug.Log(state.throttle);

	                Quaternion rotation = Quaternion.Euler(rotation_vec.x, rotation_vec.y, rotation_vec.z);
					Matrix4x4 m = Matrix4x4.Rotate(rotation);

					a.x = state.steering * 1.75f * (float)Math.Cos(rotation_vec.y * (Math.PI / 180.0));
           		 	b.x = state.steering * 2.60f * (float)Math.Cos(rotation_vec.y * (Math.PI / 180.0));

           		 	a.z = state.steering * 1.75f * -(float)Math.Sin(rotation_vec.y * (Math.PI / 180.0));
           		 	b.z = state.steering * 2.60f * -(float)Math.Sin(rotation_vec.y * (Math.PI / 180.0));

	                

	                // a.z = state.steering * 1.75f * car_obj.transform.rotation.eulerAngles.y;
	                // b.z = state.steering * 2.60f * car_obj.transform.rotation.eulerAngles.y;

	                // a = m.MultiplyPoint3x4(a);
	                // b = m.MultiplyPoint3x4(b);

	                // Vector3 tmp = car_position.position + a;
	                // tmp.y = Mathf.Clamp(tmp.y, 0f, 2.5f);

	                // Vector3 tmp_2 = car_position.position + b;
	                // tmp_2.y = Mathf.Clamp(tmp_2.y, 0f, 4.5f);



                	lr.SetPosition(0, car_position.position);
			    	lr.SetPosition(1, mid_path_position.position + a);
			        lr.SetPosition(2, end_path_position.position + b);



                	


	            }
	        }catch(WebException ex){//če bomo kaj hendlali če ne dela 
	        }
	    	

	    	// lr.positionCount = 3;
	    	// lr.SetPosition(0, car_position.position);
	    	// lr.SetPosition(1, mid_path_position.position);
	     //    lr.SetPosition(2, end_path_position.position);
	    }
	}
}