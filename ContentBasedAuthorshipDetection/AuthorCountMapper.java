
import java.io.IOException;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


public class AuthorCountMapper extends Mapper<LongWritable, Text, Text, Text>{

	public void map(LongWritable key, Text values, Context context) throws IOException, InterruptedException { 

		NGram gram = new NGram(values.toString());

		context.write(new Text("one"),new Text(gram.GetAuthorLastName()));


	}
}
