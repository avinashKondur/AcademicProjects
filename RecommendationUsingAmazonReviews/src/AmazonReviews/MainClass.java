package AmazonReviews;

import java.io.IOException;
import java.net.URISyntaxException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;

import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;



public class MainClass {

	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException, URISyntaxException {
		
		Configuration conf = new Configuration();
		//conf.set("mapred.textoutputformat.separatorText", ",");

		//System.out.println(args[0]+"==="+ args[1]);
		conf.set("mapreduce.job.maps", "4");
		conf.set("mapreduce.job.reduces", "4");
		//conf.set("mapred.child.java.opts", "-Xmx512m");
		conf.set("mapreduce.map.output.compress", "true");
		
		Job job1=Job.getInstance(conf);		
		
		job1.setJarByClass(MainClass.class);
		job1.setMapperClass(Map.class);
		job1.setReducerClass(Reduce.class);		
		job1.setOutputKeyClass(Text.class);
		job1.setOutputValueClass(Text.class);
		job1.setInputFormatClass(TextInputFormat.class);
		job1.setOutputFormatClass(TextOutputFormat.class);		
		job1.setNumReduceTasks(1000);					
		FileInputFormat.setInputPaths(job1, new Path(args[1]));
		FileOutputFormat.setOutputPath(job1, new Path(args[2]+"/ActualData"));
		job1.waitForCompletion(true);
		
		
		/*conf = new Configuration();
		conf.set("mapreduce.job.maps", "4");
		conf.set("mapreduce.job.reduces", "4");
		//conf.set("mapred.child.java.opts", "-Xmx512m");
		conf.set("mapreduce.map.output.compress", "true");*/
		
		
		Job job=Job.getInstance(conf);
		job.setJarByClass(MainClass.class);
		job.setMapperClass(OriginalRatingsMapper.class);
		job.setReducerClass(OriginalRatingsReducer.class);
		job.setNumReduceTasks(1000);	
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);
		FileInputFormat.setInputPaths(job, new Path(args[2]+"/ActualData"));
		FileOutputFormat.setOutputPath(job, new Path(args[2]+"/originalRatings"));
		job.waitForCompletion(true);
		
		
		
		
		Job job2=Job.getInstance(conf);
		job2.setJarByClass(MainClass.class);
		job2.setMapperClass(PIDMapper.class);
		job2.setReducerClass(PIDReducer.class);
		job2.setNumReduceTasks(1000);	
		job2.setOutputKeyClass(Text.class);
		job2.setOutputValueClass(Text.class);
		job2.setInputFormatClass(TextInputFormat.class);
		job2.setOutputFormatClass(TextOutputFormat.class);
		FileInputFormat.setInputPaths(job2, new Path(args[2]+"/originalRatings"));
		FileOutputFormat.setOutputPath(job2, new Path(args[2]+"/PIDList"));
		job2.waitForCompletion(true);
		
		
		Job job3=Job.getInstance(conf);
		job3.setJarByClass(MainClass.class);
		job3.setMapperClass(UIDMapper.class);
		job3.setReducerClass(UIDReducer.class);
		job3.setNumReduceTasks(1000);	
		job3.setOutputKeyClass(Text.class);
		job3.setOutputValueClass(Text.class);
		job3.setInputFormatClass(TextInputFormat.class);
		job3.setOutputFormatClass(TextOutputFormat.class);
		FileInputFormat.setInputPaths(job3, new Path(args[2]+"/originalRatings"));
		FileOutputFormat.setOutputPath(job3, new Path(args[2]+"/UIDList"));
		job3.waitForCompletion(true);
		
		conf = new Configuration();
		//conf.set("mapred.textoutputformat.separatorText", ",");

		//System.out.println(args[0]+"==="+ args[1]);
		conf.set("mapreduce.job.maps", "4");
		
		//conf.set("mapreduce.job.reduces", "4");
		//conf.set("mapred.child.java.opts", "-Xmx512m");
		conf.set("mapreduce.map.output.compress", "true");
		
		Job job4=Job.getInstance(conf);
		job4.setJarByClass(MainClass.class);
		job4.setMapperClass(PIDVectorMapper.class);
		job4.setReducerClass(PIDVectorReducer.class);
		job4.setNumReduceTasks(1000);	
		job4.setOutputKeyClass(Text.class);
		job4.setOutputValueClass(Text.class);
		job4.setInputFormatClass(TextInputFormat.class);
		job4.setOutputFormatClass(TextOutputFormat.class);
		FileInputFormat.setInputPaths(job4, new Path(args[2]+"/originalRatings"));
		FileOutputFormat.setOutputPath(job4, new Path(args[2]+"/PIDVector"));
		job4.waitForCompletion(true);
				
		
	}
	
}
