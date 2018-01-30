package AmazonReviews;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;

import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.util.CoreMap;

public class StanfordSentiment {

	public String IdentifySentiment(String reviewText){

		Properties prop = new Properties();

		prop.setProperty("annotators", "tokenize, ssplit, pos, parse, sentiment");

		StanfordCoreNLP nlp = new StanfordCoreNLP(prop);

		String [] texts = reviewText.split("[.,!;]");

		//String longestString = _getSmallestString(texts);

		//System.out.println(Arrays.toString(texts)+ texts.length);

		StringBuilder str = new StringBuilder(); 		

		
		for(String text : texts){

			Annotation doc;
			if(!text.trim().isEmpty()){
				doc = new Annotation(text);				

				nlp.annotate(doc);

				List<CoreMap> sentences = doc.get(SentencesAnnotation.class);

				//System.out.println(sentences.size());


				for(CoreMap sentenct : sentences){

					String sentiment = sentenct.get(SentimentCoreAnnotations.SentimentClass.class);
					//System.out.println(sentiment);
					str.append(sentiment).append(",");					

				}
			}

		}
		
		//System.out.println(str.toString());
		
		return str.toString().isEmpty()?"#####":str.toString().substring(0, str.toString().lastIndexOf(','));
	}




	private String _getSmallestString(String[] array) {
		int maxLength = Integer.MAX_VALUE;
		String longestString = null;
		for (String s : array) {
			if (s.length() < maxLength) {
				maxLength = s.length();
				longestString = s;
			}
		}
		return longestString;
	}

}
