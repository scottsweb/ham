<?php

class Nest
{
	public $debug;
	private $username;
	private $password;
	private $cookieFile;
	private $object_base_id;
	private $deviceid;
	private $user_id;
	private $transport_url;

	public function __construct($username, $password, $debug = false)
	{
		// Set the properties
		$this->debug	 = $debug;
		$this->username	 = $username;
		$this->password	 = $password;
		$this->useragent = 'Nest/1.1.0.10 CFNetwork/548.0.4';
		$this->cookieFile = tempnam('/tmp', 'nest-cookie');

		// Login
		$response = $this->curlPost('https://home.nest.com/user/login', 'username=' . urlencode($username) . '&password=' . urlencode($password));

		if (($json = json_decode($response)) === false)
			throw new Exception('Unable to connect to Nest');

		if (!isset($json->access_token))
			throw new Exception('Login error  '.$response);

		// Stash information needed to make subsequence requests
		$this->access_token = $json->access_token;
		$this->user_id = $json->userid;
		$this->transport_url = $json->urls->transport_url;

		// First thing to do is get the device id and the base object id to be used later on.
		// THIS HAS ONLY BEEN TESTED IN A SYSTEM WITH ONE NEST!!!
		// Reverse engineered from the website version.
		$payload = '{"known_bucket_types":["device"],"known_bucket_versions":[]}';
		$url = 'https://home.nest.com/api/0.1/user/'.$this->user_id.'/app_launch';
		$response = $this->curlPost($url, $payload);
		$response = json_decode($response, true);

		// Get device id and revision of the first device.
		$this->deviceid = $response['updated_buckets'][0]['object_key'];
		$this->object_base_id = $response['updated_buckets'][0]['object_revision'];

	}

	// Boost the hot water for the following number of minutes.
	public function setHotWaterBoost($minutes) {

		// calculate new epooch for the boost. If 0 is passed then set to 0 otherwise calculate.
		if ($minutes <= 0) $epooch = 0;
		else $epooch = time() + (60 * $minutes);

		// reverse engineered from web page, read blog if you want to know more.
		// credit to https://github.com/gboudreau/nest-api/issues/22 for help recognising that I could ignore the session variable.
		$payload = '{"objects":[{"base_object_revision":'.$this->object_base_id.',"object_key":"'.$this->deviceid.'","op":"MERGE","value":{"hot_water_boost_time_to_end":'.$epooch.'}}]}';

		//make the request
		$this->curlPost($this->transport_url . '/v5/put', $payload);

		// verify the change!
		$status = $this->getHotWaterStatus();

		if($status['hot_water_boost_time_to_end']==$epooch) {
		    $return = array("success"=>true,"code"=>200,"data"=>"Boom, hot water changed. Or you set it to the same as before.");
		} else {
		    $return = array("error"=>array( "code"=>400, "text"=>"Bad Request", "message"=>"For some reason, the hot water was not changed" ));
		}
		return json_encode($return);

	}

	public function cancelHotWaterBoost() {

		// to turn the hot water off, you need set boost time to 0
		return $this->setHotWaterBoost(0);

	}

	// this function is to verify that the setting has been applied
	public function getHotWaterStatus()
	{
		$response = $this->curlGet($this->transport_url . '/v2/mobile/user.' . $this->user_id);

		if (($json = json_decode($response, true)) === false)
			throw new Exception('Unable to gather the status from Nest');
		$device_serial = str_replace("device.","",$this->deviceid);

		return array("hot_water_active"=>$json['device'][$device_serial]['hot_water_active'],"hot_water_boost_time_to_end"=>$json['device'][$device_serial]['hot_water_boost_time_to_end']);
	}

	private function curlGet($url, $referer = null, $headers = null)
	{

		$headers[] = 'Authorization: Basic ' . $this->access_token;
		$headers[] = 'X-nl-user-id:' . $this->user_id;
		$headers[] = 'X-nl-protocol-version: 1';

		$ch = curl_init($url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_COOKIEFILE, $this->cookieFile);
		curl_setopt($ch, CURLOPT_COOKIEJAR, $this->cookieFile);
		curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
		curl_setopt($ch, CURLOPT_AUTOREFERER, true);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
		curl_setopt($ch, CURLOPT_USERAGENT, $this->useragent);
		if(!is_null($referer)) curl_setopt($ch, CURLOPT_REFERER, $referer);
		if(!is_null($headers)) curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

		// curl_setopt($ch, CURLOPT_VERBOSE, true);

		$html = curl_exec($ch);

		if(curl_errno($ch) != 0)
		{
			throw new Exception("Error during GET of '$url': " . curl_error($ch));
		}

		$this->lastURL = curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
		$this->lastStatus = curl_getinfo($ch, CURLINFO_HTTP_CODE);

		return $html;
	}

	private function curlPost($url, $post_vars = '', $referer = null)
	{
		if (isset($this->access_token)) $headers[] = 'Authorization: Basic ' . $this->access_token;
		if (isset($this->user_id)) $headers[] = 'X-nl-user-id:' . $this->user_id;
		$headers[] = 'X-nl-protocol-version: 1';

		$ch = curl_init($url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_COOKIEFILE, $this->cookieFile);
		curl_setopt($ch, CURLOPT_COOKIEJAR, $this->cookieFile);
		curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
		curl_setopt($ch, CURLOPT_AUTOREFERER, true);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
		curl_setopt($ch, CURLOPT_USERAGENT, $this->useragent);
		curl_setopt($ch, CURLOPT_POST, true);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vars);
		if(!is_null($headers)) curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

		// curl_setopt($ch, CURLOPT_VERBOSE, true);

		$html = curl_exec($ch);

		if(curl_errno($ch) != 0)
		{
			throw new Exception("Error during POST of '$url': " . curl_error($ch));
		}

		$this->lastURL = curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
		$this->lastStatus = curl_getinfo($ch, CURLINFO_HTTP_CODE);

		return $html;
	}
}
