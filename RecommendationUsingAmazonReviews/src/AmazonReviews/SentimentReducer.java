package AmazonReviews;

import java.io.IOException;
import java.util.HashMap;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;

public class SentimentReducer extends Reducer<Text, Text, Text, Text> {

	@Override
	public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {

		for (Text value : values) {
			
			HashMap<String, Integer> hm = new HashMap<String,Integer>();
			
			String[] data = value.toString().split("\t");
			
			String[] sentiments = data[2].split(",");
			
			for(String sent : sentiments){
				
				if(hm.containsKey(sent)){
					int count = hm.get(sent);
					count = count+1;
					
					hm.put(sent, count);
					
				}
				else {
					hm.put(sent,1);
				}
				
			}
			
			int PosCount = hm.get("Positive") + hm.get("Very positive");
			int NegCount = hm.get("Negative") + hm.get("Very negative");
			int NeutralCount = hm.get("Neutral");
			
			String finalSent = "";
			if(NeutralCount+PosCount > NeutralCount+NegCount){
				
				finalSent = "Positive";
			}
			else if (NeutralCount+PosCount < NeutralCount+NegCount){
				finalSent = "Negative";
			}
			else{
				finalSent = "Neutral";
			}
			
			StringBuilder str = new StringBuilder();
			
			str.append(data[0]).append("\t").append(data[1]).append("\t").append(finalSent);
			
			context.write(key,new Text(str.toString()));
		}
	}
}
