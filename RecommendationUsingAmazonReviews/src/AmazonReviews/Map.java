package AmazonReviews;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;;



public class Map extends Mapper<LongWritable, Text, Text, Text>{

	@Override
	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {


		StanfordSentiment sa = new StanfordSentiment();



		JSONParser parser = new JSONParser();			

		StringBuilder str = new StringBuilder();



		JSONObject obj2;
		try {
			obj2 = (JSONObject)parser.parse(value.toString());
			
			//str.append(obj2.get("reviewerID").toString()).append("\t");
			str.append(obj2.get("asin").toString()).append("\t");
			str.append(obj2.get("overall").toString()).append("\t");

			String reviewText = obj2.get("reviewText").toString();
			
			//System.out.println("======================= str till now============="+str.toString());
					
			if(reviewText.isEmpty())
				str.append("#####");
			else
				//	.. Identify the sentiment of the review text
				str.append(sa.IdentifySentiment(reviewText));
				//str.append("#####");
			
			//System.out.println("======================= str after sentiment============="+str.toString());
			
			context.write(new Text(obj2.get("reviewerID").toString()), new Text(str.toString()));
			
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
						
		}

		

		/*String[] pair = individuals.split("\": ");
			pair[0] = pair[0].replaceAll("\"", "");
			pair[0] = pair[0].replaceAll("[{]", "");
			pair[1] = pair[1].replaceAll("\"", "");
			pair[1] = pair[1].replaceAll("[}]", "");
			System.out.println(pair[1]);
			if(pair[0].contentEquals("reviewerID") || pair[0].contentEquals("asin") || pair[0].contentEquals("reviewText") || pair[0].contentEquals("overall")){
				dummy = dummy + "\t" + pair[1];
			}*/

	}

}
