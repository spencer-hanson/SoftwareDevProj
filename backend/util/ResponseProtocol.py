class ResponseProtocol(object):
	@staticmethod
	def doResponse(strings): #Turn an array of responses into a JSON response
		resp_str = "{\n";
		len_str = len(strings);
		for i in range(0, len_str-1):
			data_str = strings[i];
			resp_str = "{}\t\"{}\":\"{}\",\n".format(resp_str, data_str[0], data_str[1]);
		resp_str = "{}\t\"{}\":\"{}\"\n".format(resp_str, strings[len_str-1][0], strings[len_str-1][1]);
		resp_str = resp_str + "}";
		return resp_str;
