package AmazonReviews;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class MainClass2 {

	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		Configuration conf = new Configuration();
		//conf.set("mapred.textoutputformat.separatorText", ",");

		//System.out.println(args[0]+"==="+ args[1]);
		conf.set("mapreduce.job.maps", "50");
		conf.set("mapreduce.job.reduces", "1000");
		conf.set("mapreduce.map.java.opts", "-Xmx1024M");
		conf.set("mapreduce.map.memory.mb","2048");		
		conf.set("mapreduce.map.output.compress", "true");
		//conf.set("mapreduce.job.running.map.limit", "2");		
		
		Job job1=Job.getInstance(conf);		
		
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/json-20140107.jar"));
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/json-simple-1.1.jar"));
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/xom.jar"));
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/stanford-corenlp-3.6.0-models.jar"));
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/stanford-corenlp-3.6.0.jar"));
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/slf4j-simple.jar"));
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/slf4j-api.jar"));
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/protobuf.jar"));		
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/jollyday-0.4.7-sources.jar"));
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/joda-time.jar"));
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/ejml-0.23.jar"));
		job1.addArchiveToClassPath(new Path("/TermProject/Jars/javax.json.jar"));
		
		
		
		job1.setJarByClass(MainClass2.class);
		job1.setMapperClass(Map.class);
		job1.setReducerClass(Reduce.class);		
		job1.setOutputKeyClass(Text.class);
		job1.setOutputValueClass(Text.class);
		job1.setInputFormatClass(TextInputFormat.class);
		job1.setOutputFormatClass(TextOutputFormat.class);		
		//job1.setNumReduceTasks(1000);					
		FileInputFormat.setInputPaths(job1, new Path(args[0]));
		FileOutputFormat.setOutputPath(job1, new Path(args[1]+"/ActualData"));
		job1.waitForCompletion(true);

	}

}
