@Test
public void testCopy_readerToOutputStream() throws Exception {
    InputStream in = new ByteArrayInputStream ( inData );
    in = new YellOnCloseInputStreamTest ( in );
    Reader reader = new InputStreamReader ( in, "US-ASCII" );
    ByteArrayOutputStream baout = new ByteArrayOutputStream();
    OutputStream out = new YellOnFlushAndCloseOutputStreamTest ( baout, false, true );
    IOUtils.copy ( reader, out );
    assertEquals ( "Sizes differ", inData.length, baout.size() );
    assertTrue ( "Content differs", Arrays.equals ( inData, baout.toByteArray() ) );
}
