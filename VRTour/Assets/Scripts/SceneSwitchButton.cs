using UnityEngine;
using UnityEngine.SceneManagement;
using VRStandardAssets.Utils;
using UnityEngine.UI;

namespace VRStandardAssets.Examples
{
	// This script is a simple example of how an interactive item can
	// be used to change things on gameobjects by handling events.
	public class SceneSwitchButton : MonoBehaviour
	{
		[SerializeField] private VRInteractiveItem m_InteractiveItem;
		[SerializeField] private Renderer m_Renderer;
		[SerializeField] private Material normalMat;
		[SerializeField] private Material outlinedMat;
        public Text change;

		private void Awake ()
		{
			
		}


		private void OnEnable()
		{
			m_InteractiveItem.OnOver += HandleOver;
			m_InteractiveItem.OnOut += HandleOut;
			m_InteractiveItem.OnClick += HandleClick;
			m_InteractiveItem.OnDoubleClick += HandleDoubleClick;
		}


		private void OnDisable()
		{
			m_InteractiveItem.OnOver -= HandleOver;
			m_InteractiveItem.OnOut -= HandleOut;
			m_InteractiveItem.OnClick -= HandleClick;
			m_InteractiveItem.OnDoubleClick -= HandleDoubleClick;
		}


		//Handle the Over event
		private void HandleOver()
		{
			m_Renderer.material = outlinedMat;
            change.text = m_InteractiveItem.name.ToString();
        }


		//Handle the Out event
		private void HandleOut()
		{
			m_Renderer.material = normalMat;
            if (SceneManager.GetSceneByName("Main").IsValid())
            {
                change.text = "Rheingauer Dom (Geisenheim, Germany)";
            }
            else
            {
                change.text = SceneManager.GetActiveScene().name.ToString();  //gameObject.name.ToString();
            }
        }


		//Handle the Click event
		private void HandleClick()
		{
            SceneManager.LoadScene(gameObject.name);
		}


		//Handle the DoubleClick event
		private void HandleDoubleClick()
		{
            if (Input.GetKey(KeyCode.Escape))
            {
                //UnityEngine.XR.XRSettings.enabled = false;
                Application.Quit();
            }
        }
	}

}
