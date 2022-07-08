library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;
use ieee.std_logic_misc.all;

library work;

entity cache_ram is
    generic(
        ROW_BITS : integer := 16;
        WIDTH    : integer := 64;
        TRACE    : boolean := false;
        ADD_BUF  : boolean := false
        );

    port(
        clk     : in  std_logic;
        rd_en   : in  std_logic;
        rd_addr : in  std_logic_vector(ROW_BITS - 1 downto 0);
        rd_data : out std_logic_vector(WIDTH - 1 downto 0);
        wr_sel  : in  std_logic_vector(WIDTH/8 - 1 downto 0);
        wr_addr : in  std_logic_vector(ROW_BITS - 1 downto 0);
        wr_data : in  std_logic_vector(WIDTH - 1 downto 0)
        );

end cache_ram;

architecture rtl of cache_ram is

begin

    ram: entity work.sram_0rw1r1w_64_512_freepdk45
        port map(
            clk0 => clk,
            csb0 => not or_reduce( wr_sel ),
            wmask0 => wr_sel,
            addr0 => wr_addr,
            din0 => wr_data,
            clk1 => clk,
            csb1 => not rd_en,
            addr1 => rd_addr,
            dout1 => rd_data
        );
end;
